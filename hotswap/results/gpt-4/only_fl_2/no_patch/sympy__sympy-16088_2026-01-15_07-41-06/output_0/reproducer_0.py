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

def test_issue():
    from sympy import Integral, Sum, symbols, simplify

    x, y, z, n = symbols('x y z n')
    integral_simplified = simplify(Integral(x*y - z, x))
    sum_simplified = simplify(Sum(x*y, (x, 1, n)))

    try:
        assert integral_simplified == y*Integral(x, x) - z*Integral(1, x), "Integral does not simplify correctly"
        assert str(sum_simplified) == "y*Sum(x, (x, 1, n))", "Sum does not simplify correctly"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_issue()
