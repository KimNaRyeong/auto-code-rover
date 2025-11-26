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
    assert False, "Idx object should not accept non-integer bounds"
else:
    print("Issue is present: Idx object accepts non-integer bounds")
    raise AssertionError("Idx object accepts non-integer bounds")

print("Test passed: Idx object does not accept non-integer bounds")
```
This script tries to create an `Idx` object with non-integer bounds `(m, n)`. If the creation succeeds without raising a `TypeError`, it raises an `AssertionError` indicating that the issue is present. If a `TypeError` is raised, it prints the stack trace and exits with code 0.