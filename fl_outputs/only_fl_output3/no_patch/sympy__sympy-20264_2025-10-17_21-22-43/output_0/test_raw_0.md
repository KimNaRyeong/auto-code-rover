```python
from sympy import Pow, Rational, latex
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def check_issue():
    try:
        latex(Pow(Rational(1,2),-1, evaluate=False))
        assert False, "Issue should have raised a RecursionError"
    except RecursionError as e:
        print_stacktrace(e)
        assert True, "RecursionError occurred as expected"

    try:
        latex(Pow(Rational(-1,-5),-1, evaluate=False))
        assert False, "Issue should have raised a RecursionError"
    except RecursionError as e:
        print_stacktrace(e)
        assert True, "RecursionError occurred as expected"

if __name__ == "__main__":
    check_issue()
```

This `reproducer.py` file checks for the RecursionError by invoking the `latex` function with specific `Pow` and `Rational` arguments as described in the issue. It raises an `AssertionError` if the expected error doesn't occur, indicating that the issue is still present. If the issue is not present (i.e., if the RecursionError doesn't occur), the script won't raise the `AssertionError`, indicating that the issue has been resolved.