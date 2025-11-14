Here is the `reproducer.py` file to reproduce the issue:
```
import sympy as sp
import traceback
import sys

def print_stacktrace(e: Exception):
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
    sys.exit(1)

print("Issue is fixed: Idx object does not accept non-integer bounds")
sys.exit(0)
```
This script will raise an `AssertionError` when the issue is present, printing a stack trace of the issue. If the issue is fixed, it will exit with code 0.