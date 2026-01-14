from sympy import pprint, latex, var, exp, log, Rational
from sympy.abc import x, y
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_issue():
    # Test case 1
    var('x', positive=True)
    latex_result = latex(exp(-x)*log(x))
    pprint_result = pprint(exp(-x)*log(x))
    if latex_result != pprint_result:
        raise AssertionError(f"LaTeX printer inconsistent with pretty printer: {latex_result} vs {pprint_result}")

    # Test case 2
    var('x y')
    latex_result = latex(1/(x + y)/2)
    pprint_result = pprint(1/(x + y)/2)
    if latex_result != pprint_result:
        raise AssertionError(f"LaTeX printer inconsistent with pretty printer: {latex_result} vs {pprint_result}")

    # Test case 3
    var('x y', positive=True)
    latex_result = latex(Rational(1, x + y))
    pprint_result = pprint(Rational(1, x + y))
    if latex_result != pprint_result:
        raise AssertionError(f"LaTeX printer inconsistent with pretty printer: {latex_result} vs {pprint_result}")

if __name__ == "__main__":
    try:
        test_issue()
        print("All tests passed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
