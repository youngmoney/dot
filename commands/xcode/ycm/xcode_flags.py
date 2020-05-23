from os import listdir
from os.path import dirname, join
import subprocess
#import vim
#import ycm_core
#from ycm.completers.cpp.flags import _RemoveUnusedFlags

cached_xcode_flags = {}

def MakeRelativePathsInFlagsAbsolute(flags, working_directory):
    if not working_directory:
        return list( flags )
    new_flags = []
    make_next_absolute = False
    path_flags = [ '-isystem', '-I', '-iquote', '--sysroot=' ]
    for flag in flags:
        new_flag = flag

        if make_next_absolute:
            make_next_absolute = False
            if not flag.startswith( '/' ):
                new_flag = join( working_directory, flag )

        for path_flag in path_flags:
            if flag == path_flag:
                make_next_absolute = True
                break

            if flag.startswith( path_flag ):
                path = flag[ len( path_flag ): ]
                new_flag = path_flag + join( working_directory, path )
                break

        if new_flag:
            new_flags.append( new_flag )

    return new_flags

def FindXcodeProject(filename, max_depth=3):
    parent_dir = filename

    for depth in range(max_depth):
        parent_dir = dirname(parent_dir)

        for file in listdir(parent_dir):
            if '.xcodeproj' in file:
                return join(parent_dir, file)

    return None

def GetXcodeProjectFlags(project, project_dir):
    xcode_flags = {}
    try:
        stdout = subprocess.check_output('/usr/bin/xcodebuild -configuration Debug -dry-run', shell=True, cwd=project_dir)
        for line in stdout.splitlines():
            if 'clang' in line:
                args = line.split()
                # Ignore the CompileC line that may contain a clang identifier
                if 'CompileC' in args[0]:
                    continue

                try:
                    filename = args[args.index('-c') + 1]
                    #xcode_flags[filename] = _RemoveUnusedFlags(args, filename)
                    xcode_flags[filename] = args
                except ValueError as e:
                    pass
    except OSError as e:
        raise Exception('Cannot find xcodebuild executable in PATH')

    return xcode_flags

def FlagsForFile(filename):
    flags = []
    xcode_project = FindXcodeProject(filename)
    if xcode_project:
        project_dir = dirname(xcode_project)
        cached_xcode_flags = GetXcodeProjectFlags(xcode_project, project_dir)
        if filename in cached_xcode_flags:
            flags = cached_xcode_flags[filename]
            flags = MakeRelativePathsInFlagsAbsolute(flags, project_dir)

    return { 'flags': flags,
            'do_cache': True }
