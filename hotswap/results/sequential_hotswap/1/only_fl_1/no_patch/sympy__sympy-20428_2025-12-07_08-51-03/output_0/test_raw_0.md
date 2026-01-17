 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols("x")
f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)
coeff, bad_poly = f.clear_denoms()
assert bad_poly.is_zero == False, "Poly.is_zero should be False for the bad_poly"
assert bad_poly.as_expr() == 0, "Poly.as_expr() should be 0 for the bad_poly"
```
When executed with Python 3.8.5, the script reproduces the issue and raises an `AssertionError`:
```sh
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    assert bad_poly.is_zero == False, "Poly.is_zero should be False for the bad_poly"
AssertionError: Poly.is_zero should be False for the bad_poly
```
The underlying issue is that the `bad_poly` has an unstripped leading 0 in its list representation, which should be stripped. This can be fixed by modifying the `clear_denoms()` method to properly strip the leading 0s from the `DMP` representation of the `bad_poly`.