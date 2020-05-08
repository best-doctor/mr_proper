import ast
import os

from mr_proper.public_api import is_function_pure
from mr_proper.utils.ast import get_ast_tree


def test_ok_for_destructive_assignment():
    funcdef = ast.parse("""
def foo(a):
    b, c = a
    return b * c
    """.strip()).body[0]
    assert is_function_pure(funcdef)


def test_is_function_pure_fail_case():
    funcdef = ast.parse("""
def foo(a):
    print(a)
    """.strip()).body[0]
    assert not is_function_pure(funcdef)


def test_is_function_pure_fail_case_for_recursive():
    test_file_path = os.path.join(os.path.dirname(__file__), 'test_files/test.py')
    ast_tree = get_ast_tree(test_file_path)
    foo_node = ast_tree.body[0]
    assert not is_function_pure(
        foo_node,
        file_ast_tree=ast_tree,
        pyfilepath=test_file_path,
        recursive=True,
    )
