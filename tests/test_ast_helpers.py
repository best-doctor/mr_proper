import ast

from mr_proper.utils.ast import (
    get_all_funcdefs_from, is_imported_from_stdlib, get_all_global_import_nodes,
    get_local_var_names_from_loop, get_local_var_names_from_funcdef)
from mr_proper.utils.ast_pure import extract_import_info_from_import_node


def test_get_all_funcdefs_from_works_fine():
    module = ast.parse("""
def foo(a):
    async def bar():
        pass

def baz():
    pass
        """.strip())
    actual_funcdefs = get_all_funcdefs_from(module)
    assert [f.name for f in actual_funcdefs] == ['foo', 'baz', 'bar']


def test_is_imported_from_stdlib_works_fine():
    module = ast.parse("""
from ast import parse
from typing import Union
from mr_proper.common_types import AnyFuncdef
    """.strip())
    assert is_imported_from_stdlib('parse', module)
    assert is_imported_from_stdlib('Union', module)
    assert is_imported_from_stdlib('AnyFuncdef', module) is False
    assert is_imported_from_stdlib('foo', module) is None


def test_get_all_global_import_nodes_skips_local_imports():
    module = ast.parse("""
def foo():
    from local import stuff
    """.strip())
    assert not get_all_global_import_nodes(module)


def test_get_all_global_import_nodes_gets_import_inside_if():
    module = ast.parse("""
if foo:
    from local import stuff
    """.strip())
    assert len(get_all_global_import_nodes(module)) == 1


def test_get_local_var_names_from_loop_handles_tuples():
    for_node = ast.parse("""
for a, b in foo():
    pass
    """.strip()).body[0]
    assert get_local_var_names_from_loop(for_node) == ['a', 'b']


def test_extract_import_info_from_import_node_works_fine():
    import_node = ast.parse('from mr_proper import is_function_pure').body[0]
    name_node = ast.parse('is_function_pure').body[0].value
    assert all(extract_import_info_from_import_node(import_node, name_node).values())


def test_local_name_extractor_extracts_from_annotated_assignments():
    funcdef = ast.parse("""
def foo():
    a: int = 1
    """.strip()).body[0]
    assert get_local_var_names_from_funcdef(funcdef) == ['a']
