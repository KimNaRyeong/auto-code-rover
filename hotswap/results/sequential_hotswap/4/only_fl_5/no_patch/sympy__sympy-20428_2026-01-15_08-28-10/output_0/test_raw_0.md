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
    _, bad_poly = f.clear_denoms()

    assert str(bad_poly) == "Poly(0, x, domain='EX')", "Poly does not print as zero poly"
    assert bad_poly.is_zero == False, "Poly is_zero should be False for EX domain"
    assert bad_poly.as_expr().is_zero, "as_expr() does not evaluate to 0"
    try:
        bad_poly.terms_gcd()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("terms_gcd() handling of bad_poly failed") from e

    try:
        _, result = bad_poly.primitive()
        assert str(result) == "Poly(0, x, domain='EX')", "primitive() handling of bad_poly failed or behavior changed"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("primitive() handling of bad_poly failed") from e

    try:
        assert str(bad_poly.rep) == "DMP([], EX, None)", "DMP representation of bad_poly is incorrect"
    except AssertionError as e:
        print_stacktrace(e)
        raise e


if __name__ == "__main__":
    main()
```