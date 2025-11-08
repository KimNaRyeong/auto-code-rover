import docutils.parsers.rst
from docutils.statemachine import StringList

def trim_docstring(docstring):
    lines = docstring.expandtabs().splitlines()
    indent = min(len(line) - len(line.lstrip()) for line in lines[1:] if line.lstrip())
    trimmed_lines = [line[indent:].rstrip() + '\n' for line in lines]
    return ''.join(trimmed_lines)

def test():
    """test tests something.
    """

try:
    docstring = trim_docstring(test.__doc__)
    parser = docutils.parsers.rst.Parser()
    document = docutils.utils.new_document('')
    parser.parse(docstring, document)
except Exception as e:
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
    print_stacktrace(e)
    raise AssertionError("Error rendering view docstring when the first line is not empty")
else:
    print("Issue not present, exiting with code 0")
    exit(0)
