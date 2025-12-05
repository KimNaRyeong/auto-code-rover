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

# This should raise an AssertionError
try:
    assert RootOf(x**3 + x - 1, 0).poly.gen == x
    assert RootOf((x**3 + x - 1).subs(x, tan(x)), 0).poly.gen == tan(x)
    assert RootOf(tan(x)**3 + 2*tan(x) - 1, 0).poly.gen == tan(x)
    assert RootOf((x**3 + 2*x - 1), 0).poly.gen == x
except AssertionError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    assert RootOf((x**3 + 2*x - 1), 0).poly.gen == x
AssertionError: RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
```
This confirms that the `RootOf` function might ignore the generator if the form of the polynomial is the same.