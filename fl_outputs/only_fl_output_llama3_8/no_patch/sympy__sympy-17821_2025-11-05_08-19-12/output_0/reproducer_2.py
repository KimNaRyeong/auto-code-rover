import doctest
from sympy import latex, Sum
from sympy.core.sympify import SympifyError
from functools import partial

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

def test_latex_equations():
    try:
        equation = latex(Sum(i**2 for i in range(10)))
    except (SympifyError, Exception) as e:
        print_stacktrace(e)
        raise AssertionError("Failed to generate LaTeX equation")

if __name__ == "__main__":
    try:
        test_latex_equations()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed")
        exit(0)
