# reproducer.py
from sympy import symbols, cos, exp, oo

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

def test_subs_evaluates_to_infinite():
    x = symbols('x')
    try:
        # Evaluating (x + cos(x)).subs(x, oo)
        result_simple = (x + cos(x)).subs(x, oo)
        if result_simple != oo:
            raise AssertionError("Expected (x + cos(x)).subs(x, oo) to be oo, got {}".format(result_simple))

        # Evaluating (exp(x) + cos(x)).subs(x, oo)
        result_exp = (exp(x) + cos(x)).subs(x, oo)
        if result_exp.is_finite or result_exp != oo:
            raise AssertionError("Expected (exp(x) + cos(x)).subs(x, oo) to be oo, got {}".format(result_exp))

    except Exception as e:
        print_stacktrace(e)
        raise

try:
    test_subs_evaluates_to_infinite()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed. The issue has been fixed.")
exit(0)
