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

def test_poly_domain_issue():
    try:
        from sympy import symbols, Poly
        x, y, z = symbols('x y z')
        # This line should not raise an exception
        Poly(1.2*x*y*z, x, domain='RR[y,z]')
        print("Issue is fixed.")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is present.")

if __name__ == "__main__":
    test_poly_domain_issue()
