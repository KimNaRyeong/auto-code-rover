Here is the `reproducer.py` file to reproduce the issue:
```
import sympy
from sympy import symbols, ceiling

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

x = symbols('x')

try:
    # Reproduce the issue
    result_false = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    result_true = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

    # Check for inconsistent behavior
    if result_false != result_true:
        raise AssertionError("Inconsistent behavior for sympify/simplify with ceiling")

except Exception as e:
    print_stacktrace(e)
    exit(1)

print("No issue found, exiting with code 0")
exit(0)
```
This script will reproduce the issue and raise an `AssertionError` if the behavior is inconsistent. If the issue is fixed, it will print "No issue found, exiting with code 0" and exit with code 0.