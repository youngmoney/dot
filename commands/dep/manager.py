import re
import sys
import subprocess
import shutil


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
    def get_list(self, all=False):
        if all:
            return self._get_list()
        return self._filter_list(self._get_list())

    def get_leaves(self):
        return self._filter_list(self._get_leaves())

    def package_name(self, package):
        return self._package_name(package)

    def install(self, package):
        return self._install(self._install_name(package))

    def uninstall(self, package):
        return self._uninstall(self._package_name(package))

    def ignore(self, package):
        return self._ignore(self._package_name(package))

    def supports_current_platform(self):
        return True

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
    def ignore(self, package):
        if not is_mac():
            return True

        return Manager.ignore(self, package)

    def supports_current_platform(self):
        return is_mac()

    def _ignored_packages(self):
        return ["pip3", "python3", "pip", "python", "apt", "brew"]

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
        return self._run_as_list(["python3", "-m", "pip", "list", "--format", "freeze"])

    def _get_leaves(self):
        return self._run_as_list(
            ["python3", "-m", "pip", "list", "--not-required", "--format", "freeze"]
        )

    def _install(self, package):
        return self._run_manager_command(["python3", "-m", "pip", "install", package])

    def _uninstall(self, package):
        return self._run_manager_command(
            ["python3", "-m", "pip", "uninstall", "-y", package]
        )


class Cask(Manager):
    def ignore(self, package):
        if not is_mac():
            return True

        return Manager.ignore(self, package)

    def supports_current_platform(self):
        return is_mac()

    def _get_list(self):
        return self._run_as_list(["brew", "cask", "list"])

    def _install(self, package):
        return self._run_manager_command(["brew", "cask", "install", package])

    def _uninstall(self, package):
        return self._run_manager_command(["brew", "cask", "uninstall", package])


class Apt(Manager):
    def _ignored_packages(self):
        return ["apt", "brew", "pip", "pip3", "python", "python3"]

    def ignore(self, package):
        if is_mac():
            return True

        return Manager.ignore(self, package)

    def supports_current_platform(self):
        return not is_mac()

    def _get_list(self):
        l = self._run_as_list(["dpkg", "--get-selections"])
        i = []
        for item in l:
            parts = item.split()
            if len(parts) < 2:
                continue
            if parts[1] != "install":
                continue
            i.append(parts[0])
        return i

    def _get_leaves(self):
        return []

    def _install(self, package):
        return self._run_manager_command(
            [
                "sudo",
                "env",
                "DEBIAN_FRONTEND=noninteractive",
                "apt-get",
                "-y",
                "install",
                "-qq",
                package,
            ]
        )

    def _uninstall(self, package):
        return False


class Build(Manager):
    def ignore(self, package):
        return True


class Plugin(Manager):
    def _package_name(self, package):
        p = Manager._package_name(self, package)
        if "/" in p:
            p = re.sub("^.*/", "", p)
        return p

    def _get_list(self):
        return self._run_as_list(["plugin", "list"])

    def _install(self, package):
        return self._run_manager_command(["plugin", "install", package])

    def _uninstall(self, package):
        return self._run_manager_command(["plugin", "uninstall", package])


def is_mac():
    return sys.platform == "darwin"


def get_managers():
    return {
        "python3": Python3(),
        "brew": Brew(),
        "cask": Cask(),
        "apt": Apt(),
        "build": Build(),
        "bash": Plugin(),
    }


def run(args, shell=False):
    result = subprocess.run(
        args, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=shell,
    )
    returncode = result.returncode
    out = result.stdout
    if returncode != 0:
        if not out:
            out = "(no logs)"
        else:
            out = out.rstrip("\n")
        print(f"-------\nRunning `{' '.join(args)}` failed with:\n{out}\n-------")
        return False
    return True


def update():
    if is_mac():
        pass
    else:
        run(["sudo", "apt-get", "update", "-qq"])


def bootstrap():
    if is_mac():
        if not shutil.which("brew"):
            print("installing brew...")
            if not run(
                'ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"'
            ):
                return False
        run(["brew", "update"])
        brew = Brew()
        all_brew = brew.get_list(all=True)
        if "python" not in all_brew:
            print("installing python (3)...")
            if not brew.install("python"):
                return False
    else:
        run(
            [
                "sudo",
                "env",
                "DEBIAN_FRONTEND=noninteractive",
                "apt-get",
                "update",
                "-qq",
            ]
        )
        apt = Apt()
        all_apt = apt.get_list(all=True)
        if not "python3" in all_apt:
            print("installing python3...")
            if not apt.install("python3"):
                return False
        if not "python3-pip" in all_apt:
            print("installing pip3...")
            run(
                [
                    "sudo",
                    "env",
                    "DEBIAN_FRONTEND=noninteractive",
                    "apt-get",
                    "update",
                    "-qq",
                ]
            )
            if not apt.install("python3-pip"):
                return False
    return True
