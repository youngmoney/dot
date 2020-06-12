import re
import subprocess
import pty


class CLI_Wrapper:
    def _run(self, args=[], text=None):
        result = subprocess.run(
            args,
            input=text,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )
        return result.returncode, result.stdout


class Manager(CLI_Wrapper):
    def get_list(self):
        return self._filter_list(self._get_list())

    def get_leaves(self):
        return self._filter_list(self._get_leaves())

    def is_installed(self, package):
        return self._package_name(package) in self.get_list()

    def package_name(self, package):
        return self._package_name(package)

    def install(self, package):
        return self._install(self._install_name(package))

    def uninstall(self, package):
        return self._uninstall(self._package_name(package))

    def ignore(self, package):
        return self._ignore(self._package_name(package))

    def _package_version_delimiter(self):
        return "@"

    def _package_name(self, package):
        i = package.find(self._package_version_delimiter())
        if i < 0:
            return package
        return package[:i]

    def _install_name(self, package):
        return package

    def _ignored_packages(self):
        return []

    def _ignore(self, package):
        return package in self._ignored_packages()

    def _filter_list(self, l):
        if l is None:
            return None
        keep = []
        for i in l:
            cleaned = self._package_name(i)
            if not self._ignore(cleaned):
                keep.append(cleaned)
        return keep

    def _run_as_list(self, args):
        returncode, out = self._run(args)
        if returncode != 0:
            if not out:
                out = "(no logs)"
            else:
                out = out.rstrip("\n")
            print(f"-------\nRunning `{' '.join(args)}` failed with:\n{out}\n-------")
            return None
        lines = out.splitlines()
        return [line.rstrip() for line in lines]

    def _run_manager_command(self, args):
        returncode, out = self._run(args)
        if returncode != 0:
            if not out:
                out = "(no logs)"
            else:
                out = out.rstrip("\n")
            print(f"-------\nRunning `{' '.join(args)}` failed with:\n{out}\n-------")
            return False
        return True

    def _get_list(self):
        return []

    def _get_leaves(self):
        return self._get_list()

    def _install(self, package):
        return self._run_manager_command(["false"])

    def _uninstall(self, package):
        return self._run_manager_command(["false"])


class Brew(Manager):
    def _ignored_packages(self):
        return ["pip3", "python3", "brew"]

    def _get_list(self):
        return self._run_as_list(["brew", "list"])

    def _get_leaves(self):
        return self._run_as_list(["brew", "leaves"])

    def _install(self, package):
        return self._run_manager_command(["brew", "install", package])

    def _uninstall(self, package):
        return self._run_manager_command(["brew", "uninstall", package])


class Python3(Manager):
    def _ignored_packages(self):
        return ["setuptools", "wheel", "pip", "pip3", "pip2"]

    def _package_version_delimiter(self):
        return "="

    def _package_name(self, package):
        p = Manager._package_name(self, package)
        if "/" in p:
            p = re.sub("^.*/", "", p)
        return p

    def _install_name(self, package):
        p = Manager._install_name(self, package)
        if "/" in package:
            p = "git+https://" + p
        return p

    def _get_list(self):
        return self._run_as_list(["pip3", "list", "--format", "freeze"])

    def _get_leaves(self):
        return self._run_as_list(
            ["pip3", "list", "--not-required", "--format", "freeze"]
        )

    def _install(self, package):
        return self._run_manager_command(["pip3", "install", package])

    def _uninstall(self, package):
        return self._run_manager_command(["pip3", "uninstall", "-y", package])


class Cask(Manager):
    def _get_list(self):
        return self._run_as_list(["brew", "cask", "list"])

    def _install(self, package):
        return self._run_manager_command(["brew", "cask", "install", package])

    def _uninstall(self, package):
        return self._run_manager_command(["brew", "cask", "uninstall", package])


class Apt(Manager):
    def ignore(self, package):
        return True


class Build(Manager):
    def ignore(self, package):
        return True


def get_managers():
    return {
        "python3": Python3(),
        "brew": Brew(),
        "cask": Cask(),
        "apt": Apt(),
        "build": Build(),
    }
