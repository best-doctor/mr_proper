import ast
from typing import overload, Union, List, Callable, Optional
from typing_extensions import Literal

from mr_propper.common_types import AnyFuncdef, PureCheckResult
from mr_propper.pure_validators import (
    has_no_blacklisted_calls, uses_only_args_and_local_vars,
    has_returns, not_mutates_args, not_has_local_imports, not_has_forbidden_arguments_types,
    not_uses_self_or_class_vars,
)


PureValidatorType = Callable[[AnyFuncdef, Optional[ast.Module]], List[str]]


@overload
def is_function_pure(
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module,
    with_errors: Literal[False],
) -> bool:
    ...


@overload
def is_function_pure(
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module,
    with_errors: Literal[True],
) -> PureCheckResult:
    ...


def is_function_pure(
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module = None,
    with_errors: bool = False,
) -> Union[bool, PureCheckResult]:
    validators: List[PureValidatorType] = [
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
        validator_errors = validator_callable(funcdef_node, file_ast_tree)
        if validator_errors:
            is_pure = False
            errors += list(set(validator_errors))
    return (is_pure, errors) if with_errors else is_pure
