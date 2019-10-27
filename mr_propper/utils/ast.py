import ast
from typing import Optional, List

from mr_propper.common_types import AnyFuncdef


def get_ast_tree(filepath: str) -> Optional[ast.AST]:
    return None


def get_all_funcdefs_from(ast_tree: ast.AST) -> List[AnyFuncdef]:
    return []
