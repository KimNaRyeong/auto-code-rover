Here is the reproducer script:

```python
import sympy as sp
from sympy import Eq, exp, symbols
from functools import wraps

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

def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception but got nothing")
    except expected_exception as e:
        pass

y, x = symbols('y x')
f = sp.Function('f')

try:
    idiff(Eq(y*sp.exp(y), x*sp.exp(x)), y, x)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")

try:
    idiff(f(x)*sp.exp(f(x)) - x*sp.exp(x), f(x), x)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")

try:
    idiff(y*sp.exp(y) - x*sp.exp(x), y, x)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")

print("Issue fixed")
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. It will exit with code 0 when the issue is fixed.