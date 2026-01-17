# reproducer.py
from sympy import symbols, Piecewise, S, And, Le, Ge
from sympy.core.relational import Relational
from sympy.core.function import Function


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


def check_piecewise_with_conditions():
    x = symbols('x')
    cond = And(Le(x, 6), Ge(x, 1), S.Integers.contains(x))
    try:
        p2 = Piecewise((S(1), cond), (S(0), True))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Piecewise with specified conditions fails to evaluate.") from e


if __name__ == "__main__":
    check_piecewise_with_conditions()
