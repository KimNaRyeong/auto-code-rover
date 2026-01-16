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

def main():
    from sympy import symbols, Poly, sympify

    x = symbols("x")
    f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
    coeff, bad_poly = f.clear_denoms()

    try:
        assert bad_poly.is_zero is False, "Poly.is_zero must be False"
        assert bad_poly.as_expr().is_zero is True, "'as_expr().is_zero' must be True"
        assert bad_poly.rep != Poly(0, x, domain="EX").rep, "DMP representation mismatch"
        terms_gcd_result = bad_poly.terms_gcd()
    except Exception as e:
        print_stacktrace(e)
        raise

    try:
        primitive_result = bad_poly.primitive()
        assert primitive_result == (1, Poly(0, x, domain='EX')), "Poly.primitive output mismatch"
    except AssertionError as ae:
        print(ae)
    except Exception as e:
        print_stacktrace(e)
        raise

    # Check for updated handling (should not raise an exception)
    try:
        Poly(0, x).terms_gcd()
        bad_poly.terms_gcd()
        bad_poly.primitive()
        print("Issue seems to be resolved.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is still present.")

if __name__ == "__main__":
    main()
```
This script tests for a specific issue in the `Poly` class of SymPy related to clearing denominators and the handling of polynomials that end up being the zero polynomial. It asserts for the behavior of the `.is_zero` property, the `.as_expr().is_zero` call, terms gcd, and the primitive method, checking that these behave consistently and without raising unhandled exceptions. It raises an `AssertionError` if the issue is present, indicating that the problem has not been fixed. When the issue is resolved, it prints a confirmation message without raising any errors.