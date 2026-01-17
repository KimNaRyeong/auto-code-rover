import sys
from sympy import Mul, Rational, symbols, srepr

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
    x, y = symbols('x y')
    expr1 = Mul(Rational(1, 2), x + y, evaluate=False)
    expr2 = Mul(x + y, Rational(1, 2), evaluate=False)

    srepr1 = srepr(expr1)  # Use srepr for a detailed structure representation
    srepr2 = srepr(expr2)

    try:
        # Check for the presence of brackets which would indicate correct handling
        assert "Mul(Pow(Integer(2), Integer(-1)), Add(Symbol('x'), Symbol('y')))" == srepr1, \
            "The expression does not use brackets as expected for expr1"
        assert "Mul(Add(Symbol('x'), Symbol('y')), Pow(Integer(2), Integer(-1)))" == srepr2, \
            "The expression does not use brackets as expected for expr2"
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("Issue is fixed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
