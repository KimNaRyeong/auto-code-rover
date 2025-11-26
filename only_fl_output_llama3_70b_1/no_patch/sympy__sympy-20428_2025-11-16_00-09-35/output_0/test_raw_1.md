Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
from sympy import *

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

x = symbols("x")
f = Poly(sympify("-117968192370600*18**(1/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) - 15720318185*2**(2/3)*3**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 15720318185*12**(1/3)*(24201 + 253*sqrt(9165))**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3)) + 117968192370600*2**(1/3)*3**(2/3)/(217603955769048*(24201 + 253*sqrt(9165))**(1/3) + 2273005839412*sqrt(9165)*(24201 + 253*sqrt(9165))**(1/3))"), x)

coeff, bad_poly = f.clear_denoms()

assert not bad_poly.is_zero, "Issue is present"
try:
    bad_poly.terms_gcd()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue is fixed")
exit(0)
```
This script reproduces the issue by creating a polynomial `bad_poly` that prints like zero but behaves inconsistently. It then checks if `bad_poly.is_zero` is False, which should be the case if the issue is present. If it's not the case, it raises an `AssertionError`. Then, it tries to call `terms_gcd()` on `bad_poly`, which should raise an exception due to the unstripped leading 0 in the list representation of the Poly. If the exception is raised, it prints the stack trace and exits with code 1. If no exception is raised, it prints "Issue is fixed" and exits with code 0.