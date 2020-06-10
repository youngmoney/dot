import yaml
import os
import datatype
import re


def get_path():
    local = os.getenv("LOCALDOT")
    joined = os.path.join(local, "conf", "workspace.yaml")
    path = os.path.expanduser(joined)
    return path


def get_defaults_path(name="defaults.yaml"):
    script_directory, script_name = os.path.split(os.path.realpath(__file__))
    return os.path.join(script_directory, name)


def get_settings(path):
    if os.path.exists(path):
        contents = "\n".join(open(path, "r").readlines())
        obj = yaml.safe_load(contents)
        return Settings(obj)
    return None


def get():
    defaults = get_settings(get_defaults_path())
    settings = get_settings(get_path())
    if not settings:
        return defaults
    settings.creators += defaults.creators
    settings.locations += defaults.locations
    settings.layouts += defaults.layouts
    settings.commands += defaults.commands
    return settings


class Location(metaclass=datatype.Object):
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


class Creator(metaclass=datatype.Object):
    datatype_name = str
    datatype_command = str


class Direction(metaclass=datatype.Option):
    up = None
    down = None
    left = None
    right = None


class Pane(metaclass=datatype.Object):
    datatype_location_name = str
    datatype_command = str
    datatype_direction = Direction
    datatype_percent = int
    datatype_children = [datatype.Object.Self]

    def __init__(command="", direction=Direction.right, percent=50, children=[]):
        pass


class Layout(metaclass=datatype.Object):
    datatype_name = str
    datatype_location_name = str
    datatype_command = str
    datatype_children = [Pane]

    def __init__(self, children=[]):
        if not self.name:
            raise TypeError("Layout must have a name.")


class Command(metaclass=datatype.Object):
    datatype_name = str
    datatype_command = str
    datatype_path_regex = str
    datatype_path_command = str

    def __init__(self, path_regex=".*"):
        if not self.name:
            raise TypeError("Command must have a name.")


class Settings(metaclass=datatype.Object):
    datatype_locations = [Location]
    datatype_creators = [Creator]
    datatype_layouts = [Layout]
    datatype_commands = [Command]

    def __init__(self, locations=[], creators=[], layouts=[], commands=[]):
        pass

    def get_location_named(self, name):
        for location in self.locations:
            if location.name == name:
                return location
        return None

    def get_creator_named(self, name):
        for creator in self.creators:
            if creator.name == name:
                return creator
        return None

    def get_path_location(self, path):
        for location in self.locations:
            if not location.current_path_regex:
                continue
            if re.fullmatch(os.path.expanduser(location.current_path_regex), path):
                return location
        return None

    def get_layout_named(self, name):
        for layout in self.layouts:
            if layout.name == name:
                return layout
        return None

    def get_command_named(self, name):
        for command in self.commands:
            if command.name == name:
                return command
        return None
