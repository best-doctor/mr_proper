import os
import sys
import argparse

from mr_proper.public_api import is_function_pure
from mr_proper.utils.ast import get_ast_tree, get_all_funcdefs_from


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('objectname', type=str)
    parser.add_argument('--recursive', action='store_true')
    return parser.parse_args()


def checking_function(args: argparse.Namespace) -> None:
    ast_tree = get_ast_tree(args.objectname)
    if not ast_tree:
        sys.stdout.write('Error parsing ast tree\n')
        return
    sys.stdout.write(f'{args.objectname}:\n')
    for funcdef_node in get_all_funcdefs_from(ast_tree):
        function_name = funcdef_node.name
        is_pure, pureness_errors = is_function_pure(
            funcdef_node,
            ast_tree,
            with_errors=True,
            recursive=args.recursive,
            pyfilepath=args.objectname,
        )
        if is_pure:
            sys.stdout.write(f'{function_name} is pure!\n')
        else:
            sys.stdout.write(f'{function_name} is not pure because of:\n')
            for error in pureness_errors:
                sys.stdout.write(f'\t{error}\n')


def main() -> None:
    args = parse_args()
    path_to_files = [args.objectname]
    if os.path.isdir(args.objectname):
        directoty_path = os.path.abspath(args.objectname)
        path_to_files = [
            os.path.join(root, filename) for root, dirs, files in os.walk(directoty_path) for filename in files
        ]
    for path_to_file in path_to_files:
        args.objectname = path_to_file
        checking_function(args)
