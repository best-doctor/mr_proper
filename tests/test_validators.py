import ast

import pytest

from mr_proper.pure_validators import not_has_forbidden_arguments_types, not_mutates_args


@pytest.mark.parametrize(
    'funcdef_str, expected_errors',
    [
        ('def foo(a: int): pass', []),
        ('def bar(a: dict): pass', []),
        ('def baz(a: Callable): pass', ['it has type Callable in argument types']),
    ],
)
def test_not_has_forbidden_arguments_types_checks_annotations(funcdef_str, expected_errors):
    funcdef = ast.parse(funcdef_str).body[0]
    assert not_has_forbidden_arguments_types(funcdef, file_ast_tree=None) == expected_errors


@pytest.mark.parametrize(
    'funcdef_str, expected_errors',
    [
        ('def foo(a: dict): a["foo"] = 1', ['it mutates its own argument (on line 1)']),
        ('def bar(a: User): a.is_active = True', ['it mutates its own argument (on line 1)']),
        ('def baz(a: List): a.append(1)', ['it mutates its own argument (on line 1)']),
        ('def bax(a: List): return sorted(a)', []),
    ],
)
def test_not_mutates_args(funcdef_str, expected_errors):
    funcdef = ast.parse(funcdef_str).body[0]
    assert not_mutates_args(funcdef, file_ast_tree=None) == expected_errors
