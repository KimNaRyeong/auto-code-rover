Here is the reproducer script:

```python
from sympy import symbols, cos, exp, oo

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
    try:
        assert (x + cos(x)).subs(x, oo) == oo
        assert (exp(x) + cos(x)).subs(x, oo) != oo
    except AssertionError as e:
        print_stacktrace(e)
        raise
    else:
        exit(0)

if __name__ == "__main__":
    reproduce_issue()
```

You can run this script by executing `python3 reproducer.py`. If the issue is present, it will print a stack trace and raise an `AssertionError`.