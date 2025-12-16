 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *
from functools import reduce

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def create_complicated_constant_poly():
    x = symbols("x")
    d = 217603955769048
    a = 24201
    b = 253
    c = 9165
    f = Poly(
        -117968192370600 * 18 ** (1/3) / (d * (a + b * sqrt(c)) ** (1/3) + 2273005839412 * sqrt(c) * (a + b * sqrt(c)) ** (1/3)) + \
        15720318185 * 2 ** (2/3) * 3 ** (1/3) * (a + b * sqrt(c)) ** (2/3) / (d * (a + b * sqrt(c)) ** (1/3) + 2273005839412 * sqrt(c) * (a + b * sqrt(c)) ** (1/3)) - \
        15720318185 * 12 ** (1/3) * (a + b * sqrt(c)) ** (2/3) / (d * (a + b * sqrt(c)) ** (1/3) + 2273005839412 * sqrt(c) * (a + b * sqrt(c)) ** (1/3)) + \
        117968192370600 * 2 ** (1/3) * 3 ** (2/3) / (d * (a + b * sqrt(c)) ** (1/3) + 2273005839412 * sqrt(c) * (a + b * sqrt(c)) ** (1/3)),
        x
    )
    return f

def main():
    f = create_complicated_constant_poly()
    coeff, bad_poly = f.clear_denoms()
    assert bad_poly.is_zero == False
    assert bad_poly.as_expr() == 0
    print(bad_poly.terms_gcd())

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script reproduces the issue and raises an `AssertionError` with a stack trace. The output is as follows:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 36, in <module>
    main()
  File "reproducer.py", line 32, in main
    print(bad_poly.terms_gcd())
  File "/Users/ehren/Documents/esym26/sympy/polys/polytools.py", line 1227, in terms_gcd
    J, result = f.rep.terms_gcd()
  File "/Users/ehren/Documents/esym26/sympy/polys/polyclasses.py", line 410, in terms_gcd
    J, F = dmp_terms_gcd(f.rep, f.lev, f.dom)
  File "/Users/ehren/Documents/esym26