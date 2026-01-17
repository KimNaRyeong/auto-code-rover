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

    x = symbols("x")
    f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
    coeff, bad_poly = f.clear_denoms()

    # Verifying the unexpected behavior of bad_poly
    assert bad_poly.is_zero == False, "bad_poly.is_zero should not be True"
    assert bad_poly.as_expr() == 0, "The expression of bad_poly should be 0"

    try:
        terms_gcd_result = bad_poly.terms_gcd()
    except Exception as e:
        print("Failure while calling bad_poly.terms_gcd():")
        print_stacktrace(e)
        raise AssertionError("bad_poly.terms_gcd() raised an exception") from e

    try:
        primitive_result = bad_poly.primitive()
    except Exception as e:
        print("Failure while calling bad_poly.primitive():")
        print_stacktrace(e)
        raise AssertionError("bad_poly.primitive() raised an exception") from e

    # Fail if reaching this point without exceptions as it means the issue is present
    print("Issue reproduced successfully: The script executed without exceptions where one was expected.")
    print("This indicates the inconsistency in handling zero polynomials is present.")
    exit(0)

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
