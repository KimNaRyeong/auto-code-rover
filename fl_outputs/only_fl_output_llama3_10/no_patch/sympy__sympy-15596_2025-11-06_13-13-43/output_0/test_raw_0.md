Here is the `reproducer.py` file that reproduces the issue:

```python
import sympy as sp
from sympy import symbols, Rational

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
    f = Rational((x-2), (x**2+1))
    try:
        degree_value = sp.degree(f, x)
        assert degree_value == 1
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

To run the reproducer, simply execute `python3 reproducer.py` in your terminal. If the issue is present, it will print a stack trace and exit with code 1. If the issue is fixed, it will exit with code 0.