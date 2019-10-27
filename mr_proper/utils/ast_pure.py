import ast
import inspect
import importlib.util
from typing import Optional, List, cast

from mypy_extensions import TypedDict

from mr_proper.common_types import AnyFuncdef
from mr_proper.utils.ast import BUILTINS_LIST, get_nodes_from_funcdef_body, get_ast_tree


class EntityImportInfo(TypedDict):
    file_path: Optional[str]
    import_path: Optional[str]
    name: str


def get_not_pure_internal_calls(
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module,
    pyfilepath: str,
) -> List[str]:
    from mr_proper.public_api import is_function_pure

    not_pure_calls: List[str] = []
    for call_node in get_nodes_from_funcdef_body(funcdef_node, [ast.Call]):
        if not isinstance(call_node.func, ast.Name):
            continue  # recursively check only functions calls, not methods/attrs calls
        if (
            call_node.func.id.lower() == call_node.func.id  # check for only snake_case calls
            and call_node.func.id not in BUILTINS_LIST
        ):
            import_info = get_name_import_path(call_node.func, pyfilepath)
            imported_funcdef_node = get_funcdef_by(import_info) if import_info else None
            if imported_funcdef_node and import_info:
                filepath = cast(str, import_info['file_path'])
                is_call_clean: Optional[bool] = is_function_pure(
                    imported_funcdef_node,
                    file_ast_tree=file_ast_tree,
                    recursive=False,
                    pyfilepath=filepath,
                    with_errors=False,
                )
            else:
                is_call_clean = None
            if is_call_clean is False:
                not_pure_calls.append(call_node.func.id)
    return not_pure_calls


def get_name_import_path(name_node: ast.Name, pyfilepath: str) -> Optional[EntityImportInfo]:
    current_node = name_node.parent  # type: ignore
    while True:
        for child in ast.iter_child_nodes(current_node):
            # check for Import, not only ImportFrom
            if isinstance(child, ast.ImportFrom) and name_node.id in (n.name for n in child.names):
                return extract_import_info_from_import_node(child, name_node)
            elif (
                isinstance(child, (ast.FunctionDef, ast.AsyncFunctionDef))
                and child.name == name_node.id
            ):
                return {
                    'file_path': pyfilepath if pyfilepath != 'built-in' else None,
                    'import_path': None,
                    'name': name_node.id,
                }
        current_node = current_node.parent
        if not current_node:
            break
    return None


def extract_import_info_from_import_node(
    import_from_node: ast.ImportFrom,
    name_node: ast.Name,
) -> EntityImportInfo:
    import_path = import_from_node.module
    if import_path is None:
        filepath = None
    else:
        filepath = get_file_path_by(import_path, name_node.id)
        if filepath == 'built-in':
            filepath = None
    return {'file_path': filepath, 'import_path': import_from_node.module, 'name': name_node.id}


def get_funcdef_by(import_info: EntityImportInfo) -> Optional[AnyFuncdef]:
    file_path = import_info['file_path']
    if file_path:
        ast_tree = get_ast_tree(file_path)
        if not ast_tree:
            return None
        try:
            funcdef = [
                n for n in ast.walk(ast_tree)
                if (
                    isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
                    and n.name == import_info['name']
                )
            ]
        except AttributeError:
            return None
        if funcdef:
            return funcdef[0]
    return None


def get_file_path_by(
    import_path: str,
    imported_name: str,
    dynamic_resolver: bool = False,
) -> Optional[str]:
    if dynamic_resolver:
        module = importlib.import_module(import_path)
        return inspect.getfile(getattr(module, imported_name))
    else:
        try:
            module_spec = importlib.util.find_spec(import_path)
        except ModuleNotFoundError:
            return None
        return module_spec.origin if module_spec else None
