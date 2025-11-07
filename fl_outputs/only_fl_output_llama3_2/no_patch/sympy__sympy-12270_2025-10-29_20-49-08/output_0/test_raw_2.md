Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp

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

def reproduce_issue():
    x, y = sp.symbols('x y')
    expr1 = -2*x - 4*y - 8
    try:
        result = expr1.extract_multiplicatively(-2)
        assert result == 1 + 2*I, "Expected AssertionError"
    except AssertionError as e:
        print_stacktrace(e)
    else:
        print("Issue not present")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will print "Issue not present" and exit with code 0.