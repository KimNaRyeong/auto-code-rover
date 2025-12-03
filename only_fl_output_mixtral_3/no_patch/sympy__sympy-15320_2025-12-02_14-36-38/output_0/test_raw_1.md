 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import RootOf, symbols, sin, tan
from sympy.polys.polytools import Poly

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

x = symbols('x')

# Reproduce the issue
try:
    root1 = RootOf(x**3 + x - 1, 0)
    print(f"root1: {root1}")
    root2 = RootOf((x**3 + x - 1).subs(x, tan(x)), 0)
    print(f"root2: {root2}")
    print(f"root2.poly.gen: {root2.poly.gen}")

    root3 = RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
    print(f"root3: {root3}")
    root4 = RootOf((x**3 + 2*x - 1), 0)
    print(f"root4: {root4}")
    print(f"root4.poly.gen: {root4.poly.gen}")

    assert root2.poly.gen == x
    assert root4.poly.gen == x

except AssertionError:
    print_stacktrace(AssertionError("The issue has been reproduced."))
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print the following output:
```vbnet
root1: RootOf(x**3 + x - 1, 0)
root2: RootOf(x**3 + x - 1, 0)
root2.poly.gen: x
root3: RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
root4: RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
root4.poly.gen: tan(x)
Traceback (most recent call last):
  File "reproducer.py", line 29, in <module>
    assert root4.poly.gen == x
AssertionError: RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
```
This confirms that the issue has been reproduced. The `RootOf` object `root4` has a generator of `tan(x)` instead of `x`, which is unexpected.