```python
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

def reproduce_issue():
    from sympy import symbols, Poly, sympify, sqrt

    # Problematic polynomial definition
    x = symbols("x")
    f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
    coeff, bad_poly = f.clear_denoms()

    # Verify if the polynomial is recognized incorrectly
    try:
        assert bad_poly.is_zero is False, "bad_poly.is_zero should be False"
        assert bad_poly.as_expr() == 0, "bad_poly.as_expr() should equal 0"
        print("Assertions passed: Issue with .is_zero and .as_expr()")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    # Attempt to trigger specific issues with methods on bad_poly
    try:
        terms_gcd_result = bad_poly.terms_gcd()
        primitive_result = bad_poly.primitive()
        print("Methods executed without error.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    # Final check on internal representation for completeness
    expected_rep = Poly(0, x, domain="EX").rep
    if bad_poly.rep != expected_rep:
        print("Internal representation mismatch:")
        print(f"Expected: {expected_rep}, got: {bad_poly.rep}")
        exit(1)
    else:
        print("Internal representation as expected.")

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts a more thorough check based on the issue described. It first checks for the `.is_zero` and `.as_expr()` inconsistency, then moves on to test specific `Poly` class methods (`terms_gcd` and `primitive`) that may behave unexpectedly with the problematic polynomial. It uses custom checking for the internal representation at the end to ensure that the polynomial is represented as expected in the system. If any of these checks fail or an exception is encountered, the script prints a detailed stack trace and exits with a non-zero code, indicating the presence of the issue.