Here is the reproducer script:

```python
import sympy as sp
from sympy import symbols, tan

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

def reproduce_issue():
    x = symbols('x')
    t = tan(x)
    
    try:
        root1 = sp.RootOf(x**3 + x - 1, 0)
        assert root1.poly.gen == x
        root2 = sp.RootOf((x**3+x-1).subs(x,t),0)
        assert root2.poly.gen == t
        root3 = sp.RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
        assert root3.poly.gen == t
        root4 = sp.RootOf((x**3+2*x-1),0)
        assert root4.poly.gen == t
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue not reproduced")
exit(0)
```

This script will run the same tests that you did and check if the generator of `RootOf` is correctly set. If any assertion fails, it will print the stack trace and exit with code 1. Otherwise, it will print a success message and exit with code 0.