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

def test_poly_behavior():
    from sympy import symbols, Poly, sympify, sqrt

    x = symbols("x")
    f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
    coeff, bad_poly = f.clear_denoms()
    
    assert bad_poly.is_zero is False, "bad_poly.is_zero should not report True for unstripped DMP issue."
    assert str(bad_poly.rep) != "DMP([], EX, None)", "bad_poly.rep has the expected empty DMP representation, issue likely resolved."

    try:
        bad_poly.terms_gcd()
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error encountered with bad_poly.terms_gcd() indicating issue is present."

    try:
        primitive_output = bad_poly.primitive()
        assert primitive_output[0] == 1 and str(primitive_output[1]) == "Poly(0, x, domain='EX')", "Unexpected output from bad_poly.primitive(), issue may still exist."
    except Exception as e:
        print_stacktrace(e)
        assert False, "Error encountered with bad_poly.primitive() indicating issue is present."

    print("No AssertionError raised: script exited successfully with code 0, indicating the issue is likely resolved.")

if __name__ == "__main__":
    test_poly_behavior()
