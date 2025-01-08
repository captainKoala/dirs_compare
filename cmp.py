VERSION = '1.0.0'

import argparse
import filecmp
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(message):
    print(bcolors.HEADER + message + bcolors.ENDC)

def print_error(message):
    print(f'{bcolors.FAIL}ERROR: {message}{bcolors.ENDC}')

def walking_dir(path):
    walk_res = []
    walk = sorted(list(os.walk(path)), key=lambda x: (x[0], x[1]))
    for dir_path, dir_names, filenames in walk:
        walk_res.append(dir_path)
        for filename in filenames:
            walk_res.append(os.path.join(dir_path, filename))
    return walk_res

def compare_dirs(path1, path2, left_flag=True, right_flag=True, common_flag=False, diff_flag=True):
    common = []
    diff_files = []
    left_only = []
    right_only = []
    res = filecmp.dircmp(path1, path2)
    try:
        if diff_flag:
            for file_path in res.diff_files:
                diff_files.append((os.path.join(path1, file_path), os.path.join(path2, file_path)))

        if common_flag:
            for file_path in res.common_files:
                common.append((os.path.join(path1, file_path), os.path.join(path2, file_path)))

        if left_flag:
            for path in res.left_only:
                left_only.append(os.path.join(path1, path))
            only_left_dirs = [d.name for d in os.scandir(path1)
                              if d.is_dir() and d.name not in res.common_dirs]
            for dir_path in only_left_dirs:
                for path in walking_dir(os.path.join(path1, dir_path)):
                    left_only.append(path)

        if right_flag:
            for path in res.right_only:
                right_only.append(os.path.join(path2, path))
            only_right_dirs = [d.name for d in os.scandir(path2)
                               if d.is_dir() and d.name not in res.common_dirs]
            for dir_path in only_right_dirs:
                for path in walking_dir(dir_path):
                    right_only.append(path)

        for dir_path in res.common_dirs:
            subdir_common, subdir_diff_files, subdir_left_only, subdir_right_only = compare_dirs(
                os.path.join(path1, dir_path),
                os.path.join(path2, dir_path),
                left_flag=left_flag,
                right_flag=right_flag,
                common_flag=common_flag,
                diff_flag=diff_flag
            )
            common += subdir_common
            diff_files += subdir_diff_files
            left_only += subdir_left_only
            right_only += subdir_right_only
    except FileNotFoundError as e:
        print_error(f'{e.filename} does not exist')
    except NotADirectoryError as e:
        print_error(f'ERROR: {e.filename} is not a directory')
    return common, diff_files, left_only, right_only

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='python3 cmp.py', description=f'Compare two directories or files [ver.{VERSION}]')
    parser.add_argument('-p1', '--path1', '--left-path', required=True, help='Path to first (left) directory or file')
    parser.add_argument('-p2', '--path2', '--right-path', required=True, help='Path to second (right) directory or file')
    parser.add_argument('-m', '--mode', choices=['directories', 'files'], default='directories', help='Compare directories or files')
    parser.add_argument('-sc', '--show-common', action='store_true', help='Show common files')
    parser.add_argument('-hd', '--hide-diff', action='store_true', help='Hide different files')
    direction_group = parser.add_mutually_exclusive_group()
    direction_group.add_argument('-l', '--left-only', action='store_true', help='Show left only difference')
    direction_group.add_argument('-r', '--right-only', action='store_true', help='Show right only difference')

    args = parser.parse_args()
    print(f'{bcolors.OKGREEN}Compare "{args.path1}" and "{args.path2}" {args.mode} {bcolors.ENDC}')
    print_params = []
    if args.left_only:
        print_params.append('LEFT ONLY')
    if args.right_only:
        print_params.append('RIGHT ONLY')

    print_params.append('SHOW COMMON' if args.show_common else 'DO NOT SHOW COMMON')
    print_params.append('HIDE DIFFERENT' if args.hide_diff else 'DO NOT HIDE DIFFERENT')

    print(f'{bcolors.OKGREEN}{'\n'.join(print_params)}{bcolors.ENDC}')

    if args.path1 == args.path2:
        print_error('Paths must be different')
    elif args.mode == 'directories':
        common, diff_files, left_only, right_only = compare_dirs(args.path1,
                                                                 args.path2,
                                                                 left_flag=args.left_only or args.left_only == args.right_only,
                                                                 right_flag=args.right_only or args.left_only == args.right_only,
                                                                 common_flag=args.show_common,
                                                                 diff_flag=not args.hide_diff)
        if args.show_common:
            print_header(f'Common:')
            for item in sorted(common, key=lambda x: x[0]):
                print(item)
            else:
                print('No common files')

        if not args.hide_diff:
            print_header('Different files:')
            for item in sorted(diff_files):
                print(item)
            else:
                print('No different files')

        if args.left_only or args.left_only == args.right_only:
            print_header('Left only:')
            for item in sorted(left_only):
                print(item)
            if not left_only:
                print_header('No left only files')

        if args.right_only or args.left_only == args.right_only:
            print_header('Right only:')
            for item in sorted(right_only):
                print(item)
            if not right_only:
                print_header('No right only files')

    elif args.mode == 'files':
        raise NotImplementedError()
