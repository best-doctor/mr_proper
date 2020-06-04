import os
import sys
import argparse

from mr_proper.public_api import is_function_pure
from mr_proper.utils.ast import get_ast_tree, get_all_funcdefs_from


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('file_or_directory', type=str)
    parser.add_argument('--recursive', action='store_true')
    return parser.parse_args()


def check_file(path_to_file: str, recursive: bool) -> None:
    ast_tree = get_ast_tree(path_to_file)
    if not ast_tree:
        sys.stdout.write('Error parsing ast tree\n')
        return
    sys.stdout.write(f'{path_to_file}:\n')
    for funcdef_node in get_all_funcdefs_from(ast_tree):
        function_name = funcdef_node.name
        is_pure, pureness_errors = is_function_pure(
            funcdef_node,
            ast_tree,
            with_errors=True,
            recursive=recursive,
            pyfilepath=path_to_file,
        )
        if is_pure:
            sys.stdout.write(f'{function_name} is pure!\n')
        else:
            sys.stdout.write(f'{function_name} is not pure because of:\n')
            for error in pureness_errors:
                sys.stdout.write(f'\t{error}\n')


def main() -> None:
    recursive = False
    args = parse_args()
    if not os.path.exists(args.file_or_directory):
        sys.stdout.write('File or directory not exist!\n')
        return
    path_to_files = [args.file_or_directory]
    if args.recursive:
        recursive = args.recursive
    if os.path.isdir(args.file_or_directory):
        directoty_path = os.path.abspath(args.file_or_directory)
        path_to_files = [
            os.path.join(root, filename) for root, dirs, files in os.walk(directoty_path) for filename in files
        ]
    for path_to_file in path_to_files:
        check_file(path_to_file, recursive)
