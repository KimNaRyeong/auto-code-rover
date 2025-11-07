import sphinx
from typing import Tuple

def foo() -> Tuple[()]:
    """Sample text."""
    return ()

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

try:
    from sphinx import directives
    result = directives.unparse({'type': 'tuple'}, {'elements': []})
    result.pop()
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected IndexError: pop from empty list"
