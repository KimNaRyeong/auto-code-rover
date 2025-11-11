Here is the reproducer script:

```python
import sympy as sp

def reproduce_issue():
    try:
        assert sp.Float(1.0, 15)._prec != sp.Float(1.0, 16)._prec
    except AssertionError:
        print_stacktrace(Exception("Float constructor should allow to set binary precision"))
        exit(1)
    else:
        exit(0)

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

if __name__ == "__main__":
    reproduce_issue()
```

This script will create two `Float` objects with different decimal precisions and check if their binary precisions are also different. If the assertion fails, it means that the issue is present and the script will raise an exception, print the stack trace, and exit with code 1.