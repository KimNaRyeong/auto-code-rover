Here is the reproducer script:

```py
import sympy as sp
from sympy import Poly, symbols, RR
from functools import wraps

def print_stacktrace(e):
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

def assert_raises(exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        assert False, "Expected an exception"
    except exception:
        return
    assert False, "Did not raise the expected exception"

x = symbols('x')
y = symbols('y')
z = symbols('z')

def test_poly():
    Poly(1.2*x*y*z, x)

try:
    test_poly()
except OptionError as e:
    print_stacktrace(e)
else:
    assert False, "Expected an OptionError"
```

To run the script, save it to a file named `reproducer.py` and then execute it with Python: `python3 reproducer.py`.