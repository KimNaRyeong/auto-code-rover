from docutils import nodes
from docutils.parsers.rst import Directive, directives
import sphinx
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def setup(app):
    app.add_directive('pydata', PyDataDirective)

class PyDataDirective(Directive):
    has_content = True

    def run(self):
        node = nodes.paragraph()
        text = f"mol: {self.options.get('type')} = 'mol'\n\n    mole"
        node += nodes.Text(text, text)
        return [node]

def test_issue():
    sphinx.app = None
    sphinx.config = None

    rst = r"""
.. pydata:: mol
    :type: Unit
    :value: 'mol'

    mole
"""

    try:
        from .module2 import Unit  # This line should raise an error
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected the issue to be reproduced")

if __name__ == "__main__":
    test_issue()
