from sympy import Mul, Rational, symbols
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
    x, y = symbols('x y')
    expr1 = Mul(Rational(1, 2), x + y, evaluate=False)
    expr2 = Mul(x + y, Rational(1, 2), evaluate=False)

    expr1_str = str(expr1)
    expr2_str = str(expr2)

    try:
        # Here, it's assumed the issue is that expr2 should be printed using brackets around "x + y",
        # but it doesn't. Thus, the assertion checks for the incorrect behaviour.
        
        # Expected str(expr2) to show brackets around "x + y" when multiplying by Rational(1, 2) unevaluated
        correct_expr2 = "(x + y)*1/2"  # Assuming this is the "fixed" output format
        if expr2_str != correct_expr2:
            raise AssertionError(f"Output format issue: expected {correct_expr2}, got {expr2_str}")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code to indicate the presence of the issue

if __name__ == "__main__":
    main()
    print("No issues found.")  # Only prints if no AssertionError was raised
    sys.exit(0)  # Exit with success code to indicate the issue was fixed/not present

