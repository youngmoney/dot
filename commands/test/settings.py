import yaml
import os
import datatype
import re


def get_path():
    local = os.getenv("LOCALDOT")
    joined = os.path.join(local, "conf", "test.yaml")
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
    settings.tests += defaults.tests
    return settings


class Test(metaclass=datatype.Object):
    datatype_match_path_regex = str
    datatype_match_command = str
    datatype_pre_test_command = str
    datatype_test_all_command = str
    datatype_test_command = str
    datatype_test_command_search_prefix = str
    datatype_failed_log_list_command = str
    datatype_log_clean_command = str

    def __init__(self, path_regex=".*"):
        pass


class Settings(metaclass=datatype.Object):
    datatype_tests = [Test]

    def __init__(self, tests=[]):
        pass
