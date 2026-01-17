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
    from sympy import symbols, Poly, sympify, sqrt

    x = symbols("x")
    f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
    coeff, bad_poly = f.clear_denoms()
    
    # Checking for inconsistency
    try:
        assert bad_poly.is_zero is True or bad_poly.as_expr().is_zero is False, "Inconsistent zero valuation detected."
    except AssertionError as e:
        print_stacktrace(e)
        raise e
    
    # Attempt to trigger error with bad_poly.terms_gcd()
    try:
        bad_poly.terms_gcd()
    except Exception as e:  # Catch any exception to print and then check it's the expected one
        print_stacktrace(e)
    
    # Ensure we can get through the problematic function
    try:
        terms_gcd_result = bad_poly.terms_gcd()
        print("terms_gcd_result successfully returned:", terms_gcd_result)
    except Exception as e:
        print("Unexpected exception during terms_gcd:")
        print_stacktrace(e)
        raise
    
    # Checking DMP representation
    try:
        assert str(bad_poly.rep) == "DMP([], EX, None)", "bad_poly.rep does not have the expected DMP representation."
    except AssertionError as e:
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```

This Python script reproduces the originally reported issues with the `clear_denoms()` function in SymPy: inconsistency in the zero valuation of polynomials after clearing denominators, problems with the `terms_gcd()` function, and verification of the polynomial's underlying Domain Polynomial Representation (DMP) for correctness. When the issue described is present, one or more `AssertionError` exceptions or other exceptions are expected to be raised, with detailed stack traces provided for each occurrence.