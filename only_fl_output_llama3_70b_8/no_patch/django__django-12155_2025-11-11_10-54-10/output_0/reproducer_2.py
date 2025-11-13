import docutils
from docutils.parsers.rst import Directive, roles
from docutils.parsers.rst.directives import unchanged

def trim_docstring(docstring):
    lines = docstring.expandtabs().splitlines()
    indent = min(len(line) - len(line.lstrip()) for line in lines if line.lstrip())
    return '\n'.join(l.lstrip() for l in lines)

def print_stacktrace(e: Exception):
    import traceback    
    import sys    
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test():
    """test tests something.
    This is a test docstring."""

docstring = trim_docstring(test.__doc__)
parser = docutils.parsers.rst.Parser()
document = docutils.utils.new_document('test')
try:
    parser.parse(docstring, document)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Error rendering docstring")
else:
    print("Docstring rendered successfully")
