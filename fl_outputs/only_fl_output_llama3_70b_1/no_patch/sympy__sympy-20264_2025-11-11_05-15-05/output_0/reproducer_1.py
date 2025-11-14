import sympy as sp

def test_latex_conversion(expr):
    try:
        latex_expr = sp.latex(expr, mode='plain')
        print(f"Latex conversion successful: {latex_expr}")
    except Exception as e:
        print_stacktrace(e)
        assert False, "Exception occurred during latex conversion"

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

# Test cases
test_latex_conversion(sp.Pow(sp.Rational(1, 2), -1, evaluate=False))
test_latex_conversion(sp.Pow(sp.Rational(1, 2), -1, evaluate=True))

print("All tests passed successfully.")
