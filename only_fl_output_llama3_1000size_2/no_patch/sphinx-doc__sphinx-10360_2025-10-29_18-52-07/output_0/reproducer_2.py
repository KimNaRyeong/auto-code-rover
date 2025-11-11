import sphinx
from docutils import nodes
from docutils.parsers.rst import Directive

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

def my_directive(name, arguments, options, content):
    try:
        enum_value = f'  {arguments[0]}'
        sphinx.directives.enum(name, enum_value)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Enum value with attribute misparsed")

if __name__ == "__main__":
    my_directive('my_directive', ['JXL_TYPE_BOOLEAN JXL_DEPRECATED'], None, '')
