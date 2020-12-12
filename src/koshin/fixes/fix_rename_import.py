
from lib2to3.fixer_base import BaseFix
from lib2to3.fixes import fix_imports
from lib2to3.fixer_util import token, find_indentation


MAPPING = {
    'bar': 'foo.bar',
    'baz': 'foo',
}


class FixRenameImport(fix_imports.FixImports):

    run_order = 7

    mapping = MAPPING

