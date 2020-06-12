class Package:
    def __init__(self, manager="", name="", optional=False):
        self.manager = manager
        self.name = name
        self.optional = optional

    def __repr__(self):
        optional_str = "optional " if self.optional else ""
        return f"{optional_str}{self.manager} {self.name}"

    @staticmethod
    def FromString(string):
        parts = string.split(" ")
        package = Package()
        if len(parts) == 0:
            return package

        if parts[0] == "optional":
            parts = parts[1:]
            package.optional = True

        if len(parts) > 0:
            package.manager = parts[0]

        if len(parts) > 1:
            package.name = parts[1]

        return package
