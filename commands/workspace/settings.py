import yaml
import os
from datatype import DataType
import re


def get_path():
    local = os.getenv("LOCALDOT")
    joined = os.path.join(local, "conf", "workspace.yaml")
    path = os.path.expanduser(joined)
    return path


def get():
    path = get_path()
    if os.path.exists(path):
        contents = "\n".join(open(path, "r").readlines())
        obj = yaml.safe_load(contents)
        return Settings(obj)
    return None


class Location(metaclass=DataType):
    datatype_name = str
    datatype_change_path_regex = str
    datatype_change_path_command = str
    datatype_creator_name = str
    datatype_current_path_regex = str
    datatype_current_path_command = str

    def __init__(self, change_path_regex=".*"):
        if self.name is None:
            raise TypeError("Location must have a name.")


class Creator(metaclass=DataType):
    datatype_name = str
    datatype_command = str


class Settings(metaclass=DataType):
    datatype_locations = [Location]
    datatype_creators = [Creator]

    def get_location_named(self, name):
        if not self.locations:
            return None
        for location in self.locations:
            if location.name == name:
                return location
        return None

    def get_creator_named(self, name):
        if not self.creators:
            return None
        for creator in self.creators:
            if creator.name == name:
                return creator
        return None

    def get_path_location(self, path):
        if not self.locations:
            return None
        for location in self.locations:
            if not location.current_path_regex:
                continue
            if re.fullmatch(os.path.expanduser(location.current_path_regex), path):
                return location
        return None
