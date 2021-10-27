import ast
import sys
from functools import partial
from typing import overload, Union, List, Callable, Optional, Any

from mr_proper.common_types import AnyFuncdef, PureCheckResult
from mr_proper.pure_validators import (
    has_no_blacklisted_calls, uses_only_args_and_local_vars,
    has_returns, not_mutates_args, not_has_local_imports, not_has_forbidden_arguments_types,
    not_uses_self_or_class_vars,
)
from mr_proper.utils.ast_pure import get_not_pure_internal_calls

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal

PureValidatorType = Callable[[AnyFuncdef, Optional[ast.Module]], List[str]]


if sys.version_info < (3, 5, 2):
    def overload(callable_function: Callable[..., Any]) -> Callable[..., Any]:  # noqa: F811
        return callable_function


@overload
def is_function_pure(
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module,
    with_errors: Literal[False],
    recursive: bool = False,
    pyfilepath: str = None,
) -> bool:
    ...


@overload  # noqa: F811
def is_function_pure(  # noqa: F811
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module,
    with_errors: Literal[True],
    recursive: bool = False,
    pyfilepath: str = None,
) -> PureCheckResult:
    ...


def is_function_pure(  # noqa: F811
    funcdef_node: AnyFuncdef,
    file_ast_tree: ast.Module = None,
    with_errors: bool = False,
    recursive: bool = False,
    pyfilepath: str = None,
    extra_forbidden_argument_type_names: List[str] = None,
) -> Union[bool, PureCheckResult]:
    validators: List[PureValidatorType] = [
        has_no_blacklisted_calls,
        uses_only_args_and_local_vars,
        has_returns,
        not_mutates_args,
        not_has_local_imports,
        partial(
            not_has_forbidden_arguments_types,
            extra_forbidden_argument_type_names=extra_forbidden_argument_type_names,
        ),
        not_uses_self_or_class_vars,
    ]

    errors: List[str] = []
    is_pure = True
    for validator_callable in validators:
        validator_errors = validator_callable(funcdef_node, file_ast_tree)
        if validator_errors:
            is_pure = False
            errors += list(set(validator_errors))

    if recursive and file_ast_tree and pyfilepath:
        for dirty_call_name in get_not_pure_internal_calls(funcdef_node, file_ast_tree, pyfilepath):
            is_pure = False
            errors.append(f'it calls for non-pure function ({dirty_call_name})')

    return (is_pure, errors) if with_errors else is_pure
