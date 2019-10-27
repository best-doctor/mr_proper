import ast
from typing import Optional, List, Union, Type, TypeVar, cast

from mr_propper.common_types import AnyFuncdef


T = TypeVar('T', bound=ast.AST)


def get_ast_tree(pyfilepath: str) -> Optional[ast.Module]:
    with open(pyfilepath, 'r') as file_handler:
        try:
            file_content = file_handler.read()
        except UnicodeDecodeError:
            return None
    try:
        return ast.parse(file_content)
    except SyntaxError:
        return None


def get_all_funcdefs_from(ast_tree: ast.AST) -> List[AnyFuncdef]:
    return [n for n in ast.walk(ast_tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]


def get_nodes_from_funcdef_body(
    funcdef: Union[ast.FunctionDef, ast.AsyncFunctionDef],
    of_types: List[Type[T]],
) -> List[T]:
    nodes: List[ast.AST] = []
    for node in funcdef.body:
        nodes += [n for n in ast.walk(node) if isinstance(n, tuple(of_types))]
    return nodes  # type: ignore


def is_imported_from_stdlib(name: str, file_ast_tree: ast.Module) -> bool:
    return False


def get_local_var_names_from_funcdef(funcdef_node: AnyFuncdef) -> List[str]:
    local_vars_names: List[str] = []
    for assign_node in get_nodes_from_funcdef_body(funcdef_node, [ast.Assign]):
        local_vars_names += [t.id for t in assign_node.targets if isinstance(t, ast.Name)]
    for annassign_node in get_nodes_from_funcdef_body(funcdef_node, [ast.AnnAssign]):
        if isinstance(annassign_node.target, ast.Name):
            local_vars_names.append(annassign_node.target.id)
    for comprehension in get_nodes_from_funcdef_body(funcdef_node, [ast.comprehension, ast.For]):
        comprehension = cast(ast.comprehension, comprehension)
        local_vars_names += get_local_var_names_from_loop(comprehension)
    return local_vars_names


def get_local_var_names_from_loop(loop_node: Union[ast.comprehension, ast.For]) -> List[str]:
    if isinstance(loop_node.target, ast.Name):
        return [loop_node.target.id]
    elif isinstance(loop_node.target, ast.Tuple):
        return [e.id for e in loop_node.target.elts if isinstance(e, ast.Name)]
    return []
