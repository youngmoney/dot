import re
import yaml
import os
import datatype


def get_path():
    local = os.getenv("LOCALDOT")
    joined = os.path.join(local, "conf", "lint.yaml")
    path = os.path.expanduser(joined)
    return path


def get():
    path = get_path()
    if os.path.exists(path):
        contents = "\n".join(open(path, "r").readlines())
        obj = yaml.safe_load(contents)
        return Settings(obj)
    return None


class Linter(metaclass=datatype.Object):
    datatype_name = str
    datatype_command = str

    def __init__(self, command=""):
        if not self.name:
            raise TypeError("Linter must have a name.")

    def __make_command__(self, command, **kwargs):
        return command.format(**kwargs)

    def get_command(self, filename):
        return self.command.format(filename=filename)


class Matcher(metaclass=datatype.Object):
    datatype_path_regex = str
    datatype_shebang_regex = str
    datatype_linter_name = str
    datatype_fixer_name = str

    def __init__(self, path_regex=".*", shebang_regex=".*"):
        pass

    def match(self, path, shebang) -> bool:
        return re.fullmatch(self.path_regex, path) and re.fullmatch(
            self.shebang_regex, shebang
        )


class Settings(metaclass=datatype.Object):
    datatype_linters = [Linter]
    datatype_fixers = [Linter]
    datatype_matchers = [Matcher]

    def __init__(self):
        linter_names = []
        for linter in self.linters:
            linter_names.append(linter.name)
        fixer_names = []
        for fixer in self.fixers:
            fixer_names.append(fixer.name)
        for matcher in self.matchers:
            if (
                matcher.linter_name is not None
                and not matcher.linter_name in linter_names
            ):
                raise TypeError(
                    f"Matcher references nonexistant linter: {matcher.linter_name}"
                )
            if matcher.fixer_name is not None and not matcher.fixer_name in fixer_names:
                raise TypeError(
                    f"Matcher references nonexistant fixer: {matcher.fixer_name}"
                )

    def __get_shebang__(self, filename):
        try:
            with open(filename, "r") as file:
                first = file.readline().rstrip("\n")
                if re.fullmatch("#!.*", first):
                    return first
                return ""
        except:
            return ""

    def __match__(self, filename):
        shebang = self.__get_shebang__(filename)
        path = os.path.abspath(filename)
        for matcher in self.matchers:
            if matcher.match(path=path, shebang=shebang):
                return matcher

    def get_linter(self, filename):
        matcher = self.__match__(filename)
        if matcher:
            for linter in self.linters:
                if linter.name == matcher.linter_name:
                    return linter

        return None

    def get_fixer(self, filename):
        matcher = self.__match__(filename)
        if matcher:
            for fixer in self.fixers:
                if fixer.name == matcher.fixer_name:
                    return fixer

        return None
