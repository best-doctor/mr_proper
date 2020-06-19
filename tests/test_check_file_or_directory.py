import pytest

from click.testing import CliRunner
from mr_proper.main import main


@pytest.mark.parametrize(
    'file_or_directory_path, check_result',
    [
        ('/test/test_files/dir_not_exist/', 'does not exist'),
        ('/test/test_files/file_not_exist.py', 'does not exist'),
        ('tests/test_files/test.py', 'tests/test_files/test.py:' and 'foo is pure!'),
        ('tests/test_files/errored.py', 'tests/test_files/errored.py:' and 'Error parsing ast tree'),
    ],
)
def test_is_not_exist(file_or_directory_path, check_result):
    runner = CliRunner()
    test_result = runner.invoke(main, file_or_directory_path)
    assert check_result in test_result.output
