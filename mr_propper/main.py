import argparse

from mr_propper.public_api import is_function_pure
from mr_propper.utils.ast import get_ast_tree, get_all_funcdefs_from


def parse_args() -> argparse.Namespace:
    pass


def main() -> None:
    args = parse_args()
    ast_tree = get_ast_tree(args.filename)
    if not ast_tree:
        print('Error parsing ast tree')
        return
    for funcdef_node in get_all_funcdefs_from(ast_tree):
        function_name = funcdef_node.name
        is_pure, pureness_errors = is_function_pure(funcdef_node, with_errors=True)
        if is_pure:
            print(f'{function_name} is pure!')
        else:
            print(f'{function_name} is not pure because of:')
            for error in pureness_errors:
                print(f'\t{error}')
