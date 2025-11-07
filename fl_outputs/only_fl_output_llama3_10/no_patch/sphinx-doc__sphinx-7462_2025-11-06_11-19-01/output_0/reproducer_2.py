import sphinx
from typing import Tuple
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

def reproducer():
    try:
        from sphinx.ext import autodoc
        foo()  # This line should raise an IndexError: pop from empty list
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected IndexError: pop from empty list"

if __name__ == "__main__":
    reproducer()
