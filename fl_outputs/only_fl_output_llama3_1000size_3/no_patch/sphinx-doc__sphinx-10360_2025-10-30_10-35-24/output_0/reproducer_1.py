import sphinx
from sphinx.ext import autodoc
import sys
import traceback

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

def test_enum_attribute():
    try:
        from libjxl import data_types  # Import the enum definition
        doc = sphinx.builder.Builder('html', config=sphinx.config.Config())
        autodoc.AutoDocument(doc, 'data_types')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to parse enum attribute")

if __name__ == '__main__':
    try:
        test_enum_attribute()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

    sys.exit(0)
