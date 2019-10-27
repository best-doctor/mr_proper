from typing import overload, List, Tuple, Union
from typing_extensions import Literal

from mr_propper.types import AnyFuncdef


@overload
def is_function_pure(funcdef_node: AnyFuncdef, with_errors: Literal[False]) -> bool:
    ...


@overload
def is_function_pure(funcdef_node: AnyFuncdef, with_errors: Literal[True]) -> Tuple[bool, List[str]]:
    ...


def is_function_pure(funcdef_node: AnyFuncdef, with_errors: bool = False) -> Union[bool, Tuple[bool, List[str]]]:
    pass
