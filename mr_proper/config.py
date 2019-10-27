import os


CALLABLES_BLACKLIST = ['print', 'open', 'post']
ATTRIBUTES_BLACKLIST = [
    'objects', 'post', 'count', 'all', 'exists',
    'filter', 'values_list', 'values', 'save',
]
FORBIDDEN_ARGUMENT_TYPES = ['QuerySet', 'Model', 'Callable']
FORBIDDEN_ATTR_CALLS_FOR_ARGS = {
    # list mutating methods
    'append',
    'clear',
    'extend',
    'insert',
    'pop',
    'remove',
    'reverse',
    'sort',
    # dict mutation_methods
    'update',
}

TARGET_PYTHON_VERSION = os.environ.get('MR_PROPER_TARGET_PYTHON_VERSION', '3.7')
