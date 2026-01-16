Here is the `reproducer.py` file designed to check the behavior of `logcombine(log(3) - log(2))` and raise an `AssertionError` only when the issue exists, that is, when `logcombine(log(3) - log(2))` does not return `log(3/2)`. It includes the function to print the stack trace as requested.

```python
from sympy import log, logcombine, simplify
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
    expr = log(3) - log(2)
    simplified_expr = logcombine(expr)
    # Expectation: logcombine should simplify the difference to log(3/2)
    expected_expr = log(3/2)
    if simplify(simplified_expr - expected_expr) != 0:  # Checks if they are not equivalent
        raise AssertionError("logcombine(log(3) - log(2)) does not return log(3/2)")

if __name__ == "__main__":
    try:
        check_issue()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with non-zero to indicate failure
    else:
        sys.exit(0)  # Exit with zero to indicate success
```

This script performs the action you requested:
- It uses SymPy's `log`, `logcombine`, and `simplify` functions to test if `logcombine(log(3) - log(2))` simplifies correctly to `log(3/2)`.
- If the simplification does not happen as expected (indicating the issue is present), it raises an `AssertionError`.
- If the assertion is raised, the script catches the exception, prints a stack trace detailing where the error occurred, and exits with a status code of `1` to indicate failure.
- If everything works as expected (indicating the issue has been fixed), the script exits with a status code of `0`, indicating success.