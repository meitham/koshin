import glob
import logging
import os
from difflib import unified_diff
from lib2to3.main import main
from os.path import abspath, join

import pytest

# make logging less verbose
logging.getLogger('lib2to3.main').setLevel(logging.WARN)
logging.getLogger('RefactoringTool').setLevel(logging.WARN)

FIXTURE_PATH = os.path.join(os.path.dirname(__file__), 'fixtures')


def _collect_in_files_from_directory(directory):
    fixture_files = glob.glob(abspath(join(directory, '*_in.py')))
    for fixture_file in fixture_files:
        yield fixture_file


def collect_all_test_fixtures():
    for root, dirs, files in os.walk(FIXTURE_PATH):
        for in_file in _collect_in_files_from_directory(root):
            fixer_to_run = root[len(FIXTURE_PATH) + 1:] or None
            marks = []
            yield pytest.param(fixer_to_run, in_file, marks=marks)


def _get_id(argvalue):
    if argvalue is not None and argvalue.startswith(FIXTURE_PATH):
        return os.path.basename(argvalue).replace("_in.py", "")


@pytest.mark.parametrize("fixer, in_file",
                         collect_all_test_fixtures(),
                         ids=_get_id)
def test_check_fixture(in_file, fixer, tmpdir):
    if fixer:
        main("koshin.fixes",
             args=[
                 '--no-diffs', '--fix', fixer, '-w', in_file, '--nobackups',
                 '--output-dir',
                 str(tmpdir)
             ])
    else:
        main("koshin.fixes",
             args=[
                 '--no-diffs', '--fix', 'all', '-w', in_file, '--nobackups',
                 '--output-dir',
                 str(tmpdir)
             ])

    result_file_name = tmpdir.join(os.path.basename(in_file))
    assert result_file_name.exists(), '%s is missing' % result_file_name
    result_file_contents = result_file_name.readlines()

    expected_file = in_file.replace("_in.py", "_out.py")
    with open(expected_file) as fh:
        expected_contents = fh.readlines()

    # ensure the expected code is actually correct and compiles
    try:
        compile(''.join(expected_contents), expected_file, 'exec')
    except Exception as e:
        pytest.fail("FATAL: %s does not compile: %s" % (expected_file, e),
                    False)

    if result_file_contents != expected_contents:
        text = "Refactured code doesn't match expected outcome\n"
        text += ''.join(
            unified_diff(expected_contents, result_file_contents, 'expected',
                         'refactured result'))
        pytest.fail(text, False)
