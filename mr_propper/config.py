import os


CALLABLES_BLACKLIST = ['print', 'open', 'post']
ATTRIBUTES_BLACKLIST = [
    'objects', 'post', 'count', 'all', 'exists',
    'filter', 'values_list', 'values', 'save',
]

TARGET_PYTHON_VERSION = os.environ.get('MR_PROPPER_TARGET_PYTHON_VERSION', '3.7')
