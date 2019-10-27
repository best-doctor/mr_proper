from typing import overload, List, Tuple, Union
from typing_extensions import Literal

from mr_propper.common_types import AnyFuncdef


PureCheckResult = Tuple[bool, List[str]]


@overload
def is_function_pure(
    funcdef_node: AnyFuncdef,
    with_errors: Literal[False],
) -> bool:
    ...


@overload
def is_function_pure(
    funcdef_node: AnyFuncdef,
    with_errors: Literal[True],
) -> PureCheckResult:
    ...


def is_function_pure(
    funcdef_node: AnyFuncdef,
    with_errors: bool = False,
) -> Union[bool, PureCheckResult]:
    pass
