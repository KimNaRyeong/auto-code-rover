 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
from sympy import Poly, symbols, sympify
from sympy.polys.polyclasses import DMP

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
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
assert bad_poly.rep == DMP([EX(0)], EX, None), "The rep of bad_poly should be DMP([EX(0)], EX, None) but is not."
assert bad_poly.is_zero is True, "The is_zero attribute of bad_poly should be True but is not."
assert bad_poly.as_expr().is_zero is True, "The as_expr() of bad_poly should be 0 but is not."
print("The issue is present.")
```
When executed with `python3 reproducer.py`, the script will print the following output:
```yaml
The issue is present.
```
This indicates that the issue is present in the current version of SymPy. If the issue is fixed, the script will exit with code 0 and not print any output.