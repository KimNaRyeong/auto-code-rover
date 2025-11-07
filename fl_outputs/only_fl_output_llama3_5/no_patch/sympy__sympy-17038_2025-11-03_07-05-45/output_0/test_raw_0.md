Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import sympy
from sympy.core.power import isqrt

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
        n = 4503599761588224
        s = isqrt(n)
        assert s**2 <= n, "Expected True"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    sympy.__version__
    reproduce_issue()
```

This script imports the necessary modules, defines a `print_stacktrace` function to print the stack trace of an exception, and then defines a `reproduce_issue` function that attempts to reproduce the issue. The `reproduce_issue` function tries to calculate the integer square root of a given number using the `isqrt` function from SymPy's `sympy.core.power` module. If the result is incorrect (i.e., the assertion fails), it prints the stack trace and raises an `AssertionError`.