from typing import overload, Union, List
from typing_extensions import Literal

from mr_propper.common_types import AnyFuncdef, PureCheckResult
from mr_propper.pure_validators import (
    has_no_blacklisted_calls, uses_only_args_and_local_vars,
    has_returns, not_mutates_args, not_has_local_imports, not_has_forbidden_arguments_types,
    not_uses_self_or_class_vars,
)


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
    validators = [
        has_no_blacklisted_calls,
        uses_only_args_and_local_vars,
        has_returns,
        not_mutates_args,
        not_has_local_imports,
        not_has_forbidden_arguments_types,
        not_uses_self_or_class_vars,
    ]

    errors: List[str] = []
    is_pure = True
    for validator_callable in validators:
        is_validator_ok, validator_errors = validator_callable(funcdef_node)
        if not is_validator_ok:
            is_pure = False
            errors += validator_errors
    return (is_pure, errors) if with_errors else is_pure
