from sympy import symbols, Piecewise, S, And, Le, Ge
from sympy.logic.boolalg import BooleanFunction
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x = symbols('x')
    cond = And(Le(x, 6), Ge(x, 1), S.Integers.contains(x))

    try:
        p2 = Piecewise((S(1), cond), (S(0), True))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue with Piecewise processing is present.") from e

    # Assertion to fail if the condition does not evaluate correctly or has exceptions
    assert isinstance(p2.args[0][1], BooleanFunction), "The condition should be a boolean function."
    print("Issue fixed, exiting with code 0.")
    sys.exit(0)

if __name__ == "__main__":
    main()
