
"""
Fixer that changes patch('bar', x=y) into patch('foo.bar', x=y)
"""
import ast

from lib2to3 import fixer_base
from lib2to3.pytree import Node
from lib2to3.pygram import python_symbols as syms
from lib2to3.fixer_util import Name, ArgList, in_special_context, touch_import


class FixRenameMockPatch(fixer_base.BaseFix):

    PATTERN = """
    power<
        'patch' args=trailer< '(' [any] ')' >
        |
        decorator< '@' dotted_name< 'mock' '.' 'patch' > '(' [any] ')' '\\n' >
    >
    """

    def transform(self, node, results):
        if in_special_context(node):
            return None

        args = results['args'].clone()
        args.prefix = ""
        mocked = args.children[1].value
        try:
            mocked = ast.literal_eval(mocked)
        except (SyntaxError, ValueError):
            args.children[1].value = f'foo.{mocked}'
            # touch_import('foo', mocked, node)
        else:
            args.children[1].value = f"'foo.{mocked}'"

        name = node.children[0].value
        new = Node(syms.power, [Name(name), args], prefix=node.prefix)
        return new

