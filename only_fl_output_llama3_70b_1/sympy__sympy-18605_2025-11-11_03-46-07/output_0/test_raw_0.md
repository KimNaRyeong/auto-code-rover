Here is the `reproducer.py` file that reproduces the issue:
```
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

m, n = sp.symbols("m, n", real=True)

try:
    i = sp.Idx("i", (m, n))
except TypeError as e:
    print_stacktrace(e)
else:
    raise AssertionError("Idx object accepted non-integer bounds")
```
This script will try to create an `Idx` object with non-integer bounds `(m, n)`. If the creation succeeds without raising a `TypeError`, it will raise an `AssertionError` indicating that the issue is present. If a `TypeError` is raised, it will print the stack trace of the error and exit with code 0.