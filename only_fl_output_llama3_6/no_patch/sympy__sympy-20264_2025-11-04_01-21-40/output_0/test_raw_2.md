Here is a standalone Python file `reproducer.py` that reproduces the issue:

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
    try:
        from sympy import latex
        expr = sp.Pow(sp.Rational(1, 2), -1, evaluate=False)
        print(latex(expr))
    except RecursionError as e:
        print_stacktrace(e)
    else:
        print("Issue not present. Exiting with code 0.")
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script should raise a `RecursionError` when the issue is present and print a stack trace of the issue. When the issue is fixed, it should print "Issue not present. Exiting with code 0." and exit with code 0.