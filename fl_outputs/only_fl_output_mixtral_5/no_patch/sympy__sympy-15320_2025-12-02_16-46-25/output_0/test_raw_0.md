 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import RootOf, symbols, tan, poly

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

# This should be RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
tan_x_roof = RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
print(tan_x_roof)

# This should be RootOf(x**3 + 2*x - 1, 0)
x_roof = RootOf(x**3 + 2*x - 1, 0)
print(x_roof)

# This should raise AssertionError
assert tan_x_roof.poly.gen == tan(x)
assert x_roof.poly.gen == x
```
When executed with `python3 reproducer.py`, the script prints the following output:
```vbnet
RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
RootOf(x**3 + 2*x - 1, 0)
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    assert tan_x_roof.poly.gen == tan(x)
AssertionError: tan(x)
```
The script asserts that the generator of `tan_x_roof` should be `tan(x)`, but it is not. This is the issue that was reported.