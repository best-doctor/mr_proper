import ast
import builtins
from typing import List, Optional, Callable, cast

from mr_propper.common_types import AnyFuncdef
from mr_propper.config import (
    CALLABLES_BLACKLIST, ATTRIBUTES_BLACKLIST, FORBIDDEN_ARGUMENT_TYPES,
    FORBIDDEN_ATTR_CALLS_FOR_ARGS)
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
    subfunctions_arguments = {
        a.arg
        for n in get_nodes_from_funcdef_body(funcdef_node, [ast.FunctionDef, ast.AsyncFunctionDef])
        for a in n.args.args  # type: ignore
    }

    nonlocal_names = list(
        set(all_names)
        - set(args_names)
        - set(local_vars_names)
        - set(called_names)
        - subfunctions_arguments
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
    if not get_nodes_from_funcdef_body(funcdef_node, [ast.Return]):
        return ['it has no returns']
    return []


def not_mutates_args(funcdef_node: AnyFuncdef, file_ast_tree: Optional[ast.Module]) -> List[str]:
    args_names = {a.arg for a in funcdef_node.args.args}
    mutating_actions = [  # noqa
        (  # n +=
            ast.AugAssign,
            lambda n: True,
            lambda n: n.target,
        ),
        (  # n[...] =
            ast.Assign,
            lambda n: (
                n.targets
                and isinstance(n.targets[0], ast.Subscript)
                and isinstance(n.targets[0].value, ast.Name)
                and n.targets[0].value.id in args_names
            ),
            lambda n: n.targets[0],
        ),
        (  # n.foo =
            ast.Assign,
            lambda n: n.targets and isinstance(n.targets[0], ast.Attribute),
            lambda n: n.targets[0].value,
        ),
        (  # n.append/remove/...(...)
            ast.Attribute,
            lambda n: (
                n.attr in FORBIDDEN_ATTR_CALLS_FOR_ARGS
                and isinstance(n.value, ast.Name)
                and n.value.id in args_names
            ),
            lambda n: n.value,
        ),
    ]

    errors: List[str] = []
    for node_type, node_validator, node_extractor in mutating_actions:
        node_validator = cast(Callable[[ast.AST], bool], node_validator)
        node_extractor = cast(Callable[[ast.AST], ast.AST], node_extractor)
        for node in get_nodes_from_funcdef_body(funcdef_node, [node_type]):
            if not node_validator(node):
                continue
            for name_node in [n for n in ast.walk(node_extractor(node)) if isinstance(n, ast.Name)]:
                if name_node.id in args_names:
                    errors.append(f'it mutates its own argument (on line {node.lineno})')
    return errors


def not_has_local_imports(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    if get_nodes_from_funcdef_body(funcdef_node, [ast.ImportFrom, ast.Import]):
        return ['it has local imports']
    return []


def not_has_forbidden_arguments_types(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    errors: List[str] = []
    for argument in funcdef_node.args.args:
        if not argument.annotation:
            continue
        for annotation_part_node in ast.walk(argument.annotation):
            if not isinstance(annotation_part_node, ast.Name):
                continue
            type_without_prefix = annotation_part_node.id.split('.')[-1]
            if type_without_prefix in FORBIDDEN_ARGUMENT_TYPES:
                errors.append(f'it has type {type_without_prefix} in argument types')
    return errors


def not_uses_self_or_class_vars(
    funcdef_node: AnyFuncdef,
    file_ast_tree: Optional[ast.Module],
) -> List[str]:
    forbidden_names = {'self', 'cls', 'super'}

    errors: List[str] = []
    for name_node in get_nodes_from_funcdef_body(funcdef_node, [ast.Name]):
        if name_node.id in forbidden_names:
            errors.append(f'it uses {name_node.id} var')
    return errors
