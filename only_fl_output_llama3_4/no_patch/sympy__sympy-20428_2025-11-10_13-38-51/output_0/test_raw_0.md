Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp

def reproduce_issue():
    x = sp.symbols("x")
    f = sp.Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
    coeff, bad_poly = f.clear_denoms()
    if not bad_poly.is_zero and bad_poly.as_expr() == 0:
        raise AssertionError("bad_poly is not zero but as_expr() evaluates to 0")
    try:
        bad_poly.terms_gcd()
    except IndexError:
        print_stacktrace()
    try:
        bad_poly.primitive()
    except ZeroDivisionError:
        print_stacktrace()

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by calling `clear_denoms()` on a complicated constant polynomial, checking if the resulting poly is not zero but as_expr() evaluates to 0, and then attempting to call `terms_gcd()` and `primitive()` methods on the poly. If any of these operations fail or produce unexpected results, an `AssertionError` is raised with a stack trace printed using the provided function.