from mr_propper.common_types import PureCheckResult, AnyFuncdef


def has_no_blacklisted_calls(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return True, []


def uses_only_args_and_local_vars(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return True, []


def has_returns(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return True, []


def not_mutates_args(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return False, []


def not_has_local_imports(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return True, []


def not_has_forbidden_arguments_types(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return True, []


def not_uses_self_or_class_vars(funcdef_node: AnyFuncdef) -> PureCheckResult:
    return True, []
