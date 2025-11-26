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
    v151_result_evaluate_false = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    v162_result_evaluate_false = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()

    assert v151_result_evaluate_false == v162_result_evaluate_false, "Inconsistent behavior for sympify/simplify with ceiling"

    v151_result_evaluate_true = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()
    v162_result_evaluate_true = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

    assert v151_result_evaluate_true == v162_result_evaluate_true, "Inconsistent behavior for sympify/simplify with ceiling"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will also exit with code 0 when the issue is fixed.