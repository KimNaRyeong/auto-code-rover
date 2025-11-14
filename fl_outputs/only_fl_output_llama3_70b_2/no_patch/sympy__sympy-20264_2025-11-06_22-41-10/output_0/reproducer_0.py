import sympy as sp

def test_latex_conversion():
    # Test cases that should raise a RecursionError
    test_cases = [
        sp.Pow(sp.Rational(1, 2), -1, evaluate=False),
        sp.Pow(sp.Rational(-1, -5), -1, evaluate=False)
    ]

    for expr in test_cases:
        try:
            latex_expr = sp.latex(expr)
            print(f"Latex conversion successful: {latex_expr}")
        except RecursionError as e:
            print_stacktrace(e)
            assert False, "RecursionError occurred while converting to Latex"

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

if __name__ == "__main__":
    test_latex_conversion()
