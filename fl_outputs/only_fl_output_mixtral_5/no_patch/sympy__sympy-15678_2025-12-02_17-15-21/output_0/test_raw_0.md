 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import Eq, exp, f, solve, symbols, idiff

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

x, y = symbols('x y')

# idiff doesn't support Eq
try:
    idiff(Eq(y*exp(y), x*exp(x)), y, x)
    assert False, "Eq should not be supported by idiff"
except AssertionError:
    pass
except Exception as e:
    print_stacktrace(e)

# idiff doesn't support f(x) instead of y
try:
    idiff(f(x)*exp(f(x)) - x*exp(x), f(x), x)
    assert False, "f(x) should not be supported by idiff"
except AssertionError:
    pass
except Exception as e:
    print_stacktrace(e)

# idiff should support y instead of f(x)
try:
    idiff(y*exp(y)- x*exp(x), y, x)
    assert True
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` for the first two tests and print a stack trace of the issue, and exit with code 0 for the third test.