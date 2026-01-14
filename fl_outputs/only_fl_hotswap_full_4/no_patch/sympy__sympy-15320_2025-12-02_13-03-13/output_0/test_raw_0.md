 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import RootOf, symbols, poly, tan

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
assert RootOf(x**3 + x - 1, 0).poly.gen == x, "AssertionError: RootOf should have x as its generator"

# This should raise an AssertionError
try:
    RootOf((x**3 + x - 1).subs(x, tan(x)), 0)
    assert False, "AssertionError: Should not be able to create this RootOf object without raising an exception"
except Exception as e:
    print_stacktrace(e)

# This should raise an AssertionError
try:
    RootOf(tan(x)**3 + 2*tan(x) - 1, 0).poly.gen
    assert False, "AssertionError: RootOf should have tan(x) as its generator"
except Exception as e:
    print_stacktrace(e)

# This should raise an AssertionError
try:
    RootOf((x**3 + 2*x - 1), 0)
    assert False, "AssertionError: Should not be able to create this RootOf object without raising an exception"
except Exception as e:
    print_stacktrace(e)

# This should not raise an AssertionError
try:
    RootOf(tan(x)**3 + 2*tan(x) - 1, 0).poly.gen == tan(x)
except Exception as e:
    print_stacktrace(e)

# This should not raise an AssertionError
try:
    RootOf((x**3 + 2*x - 1), 0).poly.gen == x
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise `AssertionError` for the lines that are expected to fail, and print a stack trace for those lines. The script should exit with code 0 when the issue is fixed.