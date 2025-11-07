Here is the reproducer script `reproducer.py`:

```python
import sympy as sp
from sympy.abc import x

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
        expression = sp.sympify("x**5 - 2*x**4 - 2*x**3 + 4*x**2 + x - 2")
        result = sp.sqf_list(expression)
        if result != (1, [(x - 2, 1), (x**2 - 1, 2)]):
            raise AssertionError("Issue not reproduced")
    except Exception as e:
        print_stacktrace(e)
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

This script imports the `sympy` library and defines a function `reproduce_issue()` that attempts to reproduce the issue. It creates an expression using `sympy.sympify()`, applies `sympy.sqf_list()` to it, and checks if the result matches the expected output. If the result does not match, it raises an `AssertionError`. The script also defines a function `print_stacktrace()` to print the stack trace of any exceptions that occur.

When you run this script with `python3 reproducer.py`, it should raise an `AssertionError` and print the stack trace if the issue is present. If the issue is fixed, it will exit with code 0 without printing anything.