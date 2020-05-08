import pytest

from mr_proper.utils.python_naming import is_python_class_name


@pytest.mark.parametrize(
    'input_str, is_class_name',
    [
        ('user', False),
        ('User', True),
    ],
)
def test_is_python_class_name(input_str, is_class_name):
    assert is_python_class_name(input_str) == is_class_name
