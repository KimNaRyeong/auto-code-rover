Here is the reproducer script:

```python
import sympy as sm
import sys
from traceback import extract_tb, print_exception

def print_stacktrace(e: Exception):
    print("Traceback (most recent call last):", file=sys.stderr)
    tb = extract_tb(e.__traceback__)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        M = sm.eye(6)
        V = 2 * sm.ones(6, 2)
        result = M.col_insert(3, V)
        if not isinstance(result, sm.Matrix):
            raise AssertionError("Expected a Matrix but got something else")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to reproduce the issue by calling `M.col_insert(3, V)`. If an exception is raised during this operation, it will be caught and printed using the provided `print_stacktrace` function. The script will then exit with a non-zero status code (1).