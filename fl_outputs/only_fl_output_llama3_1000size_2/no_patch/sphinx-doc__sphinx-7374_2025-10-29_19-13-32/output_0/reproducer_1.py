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

def rst_directive(name, content):
    if "_" in name:
        raise AssertionError("Expected underscores to be replaced with dashes")

rst_directive("example_python_function", "Some function.")

if __name__ == "__main__":
    try:
        rst_directive("example_python_function", "Some function.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
