Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp
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

def assert_raises(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception to be raised")
    except Exception as e:
        return e

def reproduce_issue():
    x = sp.symbols('x')
    t = sp.symbols('t')

    root1 = sp.RootOf(x**3+x-1, 0)
    root2 = sp.RootOf((x**3+x-1).subs(x,t), 0)

    assert root2.poly.gen == t, "RootOf might ignore generator"

    root3 = sp.RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
    root4 = sp.RootOf((x**3+2*x-1), 0)

    if root4.poly.gen != x:
        raise AssertionError("RootOf might ignore generator")

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, it will simply exit with code 0.