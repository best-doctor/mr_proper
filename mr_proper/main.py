import sys
import argparse

from mr_proper.public_api import is_function_pure
from mr_proper.utils.ast import get_ast_tree, get_all_funcdefs_from


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument('--recursive', action='store_true')
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    ast_tree = get_ast_tree(args.filename)
    if not ast_tree:
        sys.stdout.write('Error parsing ast tree\n')
        return
    for funcdef_node in get_all_funcdefs_from(ast_tree):
        function_name = funcdef_node.name
        is_pure, pureness_errors = is_function_pure(
            funcdef_node,
            ast_tree,
            with_errors=True,
            recursive=args.recursive,
            pyfilepath=args.filename,
        )
        if is_pure:
            sys.stdout.write(f'{function_name} is pure!\n')
        else:
            sys.stdout.write(f'{function_name} is not pure because of:\n')
            for error in pureness_errors:
                sys.stdout.write(f'\t{error}\n')
