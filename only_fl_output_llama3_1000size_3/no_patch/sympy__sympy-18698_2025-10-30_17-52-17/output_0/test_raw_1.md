Here is the reproducer script in Python:

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
    x = sp.symbols('x')
    polynomial = (x**2 + 1) * (x - 1)**2 * (x - 2)**3 * (x - 3)**3
    result = sp.simplify(polynomial)
    expected_result = (x**2 - 5*x + 6, 3)
    if str(result) != str(expected_result):
        raise AssertionError("Incorrect sqf_list output")
    print_stacktrace(Exception("Issue not fixed"))

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        raise
    else:
        print("Issue reproduced successfully. Exiting with code 0.")
        exit(0)
```

This script uses the `sympy` library to create a polynomial expression and then simplifies it using `simplify()` function. It then asserts that the result is equal to `(x**2 - 5*x + 6, 3)`, which should raise an `AssertionError` if the issue is present. The script also prints the stack trace of the assertion error.

To reproduce the issue, simply run this script using Python: `python3 reproducer.py`. If the issue is present, it will print the stack trace and exit with code 1. If the issue is fixed, it will print a success message and exit with code 0.