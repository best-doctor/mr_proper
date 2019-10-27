import ast
from typing import Optional, List

from mr_propper.common_types import AnyFuncdef


def get_ast_tree(pyfilepath: str) -> Optional[ast.AST]:
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
