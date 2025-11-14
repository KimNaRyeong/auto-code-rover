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

    try:
        x = symbols("x")
        f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
        _, bad_poly = f.clear_denoms()
        
        assert bad_poly.is_zero == False, "Poly.is_zero is unexpectedly False when it should be True."
        
        try:
            _ = bad_poly.terms_gcd()
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("bad_poly.terms_gcd() raised an error, indicating the issue is present.") from None

        try:
            _ = bad_poly.primitive()  # This may raise in earlier versions, but shouldn't in the fixed version.
        except Exception as e:
            print_stacktrace(e)
            raise AssertionError("bad_poly.primitive() raised an error, indicating the issue is not completely fixed yet.") from None

        # Check for unstripped leading zero in bad_poly
        if hasattr(bad_poly, 'rep') and str(bad_poly.rep).startswith('DMP([EX(0)], EX'):
            raise AssertionError("Unstripped leading zero in bad_poly representation indicates the issue is present.")

    except AssertionError as ae:
        print_stacktrace(ae)
        raise

if __name__ == "__main__":
    main()
```