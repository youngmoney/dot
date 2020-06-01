import yaml
import os
from datatype import DataType, Option
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
    datatype_layout_name = str

    def __init__(self, change_path_regex=".*"):
        if not self.name:
            raise TypeError("Location must have a name.")


class Creator(metaclass=DataType):
    datatype_name = str
    datatype_command = str


class Direction(metaclass=Option):
    up = None
    down = None
    left = None
    right = None


class Pane(metaclass=DataType):
    datatype_location_name = str
    datatype_command = str
    datatype_direction = Direction
    datatype_percent = int
    datatype_children = [DataType.Self]

    def __init__(command="", direction=Direction.right, percent=50, children=[]):
        pass


class Layout(metaclass=DataType):
    datatype_name = str
    datatype_location_name = str
    datatype_command = str
    datatype_children = [Pane]

    def __init__(self):
        if not self.name:
            raise TypeError("Layout must have a name.")


class Settings(metaclass=DataType):
    datatype_locations = [Location]
    datatype_creators = [Creator]
    datatype_layouts = [Layout]

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

    def get_layout_named(self, name):
        if not self.layouts:
            return None
        for layout in self.layouts:
            if layout.name == name:
                return layout
        return None
