import ast

from mr_proper.public_api import is_function_pure


def test_ok_for_destructive_assignment():
    funcdef = ast.parse("""
        def foo(a):
            b, c = a
            return b * c
    """.strip()).body[0]
    assert is_function_pure(funcdef)
