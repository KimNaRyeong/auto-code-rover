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

def test_mul_brackets():
    from sympy import Mul, Rational, symbols
    x, y = symbols('x y')

    # The issue manifests in how expressions are printed,
    # not in their actual structure, so we convert the expressions to strings.
    expr1 = str(Mul(Rational(1, 2), x + y, evaluate=False))
    expr2 = str(Mul(x + y, Rational(1, 2), evaluate=False))

    # Expected behavior: both expressions should be printed in a way that makes
    # their structure clear, potentially using brackets to indicate the operation order.
    expected_expr1 = "(x + y)/2"
    expected_expr2 = "(x + y)*1/2"  # or any similar clear notation that preserves operation order

    assert expr1 == expected_expr1, f"Expression 1 printed incorrectly: {expr1}"
    assert expr2 == expected_expr2, f"Expression 2 printed incorrectly: {expr2}"

if __name__ == "__main__":
    try:
        test_mul_brackets()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Use non-zero exit code to indicate failure
    else:
        print("Issue not found. Exiting with code 0.")
        sys.exit(0)
