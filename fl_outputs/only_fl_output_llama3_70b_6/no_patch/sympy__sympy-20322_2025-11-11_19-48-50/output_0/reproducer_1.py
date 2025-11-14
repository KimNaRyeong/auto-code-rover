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

v151_result = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
v162_result_evaluate_false = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()

try:
    assert v151_result == v162_result_evaluate_false, "Inconsistent behavior for sympify/simplify with ceiling"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

v162_result_evaluate_true = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

try:
    assert v162_result_evaluate_false == v162_result_evaluate_true, "Inconsistent behavior for sympify/simplify with ceiling"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed")
exit(0)
