import ast
from typing import Union, Tuple, List


AnyFuncdef = Union[ast.FunctionDef, ast.AsyncFunctionDef]
PureCheckResult = Tuple[bool, List[str]]
