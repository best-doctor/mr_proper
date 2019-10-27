import ast
import builtins
from typing import List, Optional

from mr_propper.common_types import AnyFuncdef
from mr_propper.config import CALLABLES_BLACKLIST, ATTRIBUTES_BLACKLIST
from mr_propper.utils.ast import (
    get_nodes_from_funcdef_body, is_imported_from_stdlib,
    get_local_var_names_from_funcdef,
)
from mr_propper.utils.python_naming import is_python_class_name

BUILTINS_LIST = {b for b in dir(builtins) if not b.startswith('_')}


def has_no_blacklisted_calls(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    errors: List[str] = []
    for call_node in [n for n in ast.walk(funcdef_node) if isinstance(n, ast.Call)]:
        if isinstance(call_node.func, ast.Name) and call_node.func.id in CALLABLES_BLACKLIST:
            errors.append(f'it calls forbidden function ({call_node.func.id})')
    for attr_node in [n for n in ast.walk(funcdef_node) if isinstance(n, ast.Attribute)]:
        if attr_node.attr in ATTRIBUTES_BLACKLIST:
            errors.append(f'it accesses forbidden attribute ({attr_node.attr})')
    return errors


def uses_only_args_and_local_vars(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
    allow_external_class_usage: bool = False,
    allow_stdlib_usage: bool = True,
) -> List[str]:
    all_names = [n.id for n in get_nodes_from_funcdef_body(funcdef_node, [ast.Name])]
    args_names = [a.arg for a in funcdef_node.args.args]
    called_names = [
        c.func.id
        for c in get_nodes_from_funcdef_body(funcdef_node, [ast.Call])
        if isinstance(c.func, ast.Name)
    ]
    local_vars_names = get_local_var_names_from_funcdef(funcdef_node)

    nonlocal_names = list(
        set(all_names)
        - set(args_names)
        - set(local_vars_names)
        - set(called_names)
        - BUILTINS_LIST,
    )
    if allow_external_class_usage:
        nonlocal_names = [n for n in nonlocal_names if not is_python_class_name(n)]
    if allow_stdlib_usage and file_ast_tree:
        nonlocal_names = [
            n for n in nonlocal_names
            if not is_imported_from_stdlib(n, file_ast_tree)
        ]

    return [f'it uses external name ({n})' for n in nonlocal_names]


def has_returns(funcdef_node: AnyFuncdef, file_ast_tree: Optional[ast.Module]) -> List[str]:
    return []


def not_mutates_args(funcdef_node: AnyFuncdef, file_ast_tree: Optional[ast.Module]) -> List[str]:
    return []


def not_has_local_imports(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    return []


def not_has_forbidden_arguments_types(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    return []


def not_uses_self_or_class_vars(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    return []
