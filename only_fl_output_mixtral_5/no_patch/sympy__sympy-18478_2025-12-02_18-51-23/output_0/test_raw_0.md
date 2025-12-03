 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import symbols, Function, exp, cos, oo, sin, pi, pprint, Subs
from sympy.abc import x

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

def main():
    x = symbols('x', real=True)
    f = Function('f')

    # Reproduce the issue
    expr1 = x + cos(x)
    expr2 = exp(x) + cos(x)

    # expr1.subs(x, oo) should be oo, but it's not
    subs1 = expr1.subs(x, oo)
    if subs1 != oo:
        e = AssertionError(f"expr1.subs(x, oo) should be oo, but it's not: {subs1}")
        print_stacktrace(e)
        raise e

    # expr2.subs(x, oo) should be AccumBounds, but it's not
    subs2 = expr2.subs(x, oo)
    if subs2 != subs2.func(AccumBounds):
        e = AssertionError(f"expr2.subs(x, oo) should be AccumBounds, but it's not: {subs2}")
        print_stacktrace(e)
        raise e

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with a stack trace, indicating that the issue is present. If the issue is fixed, the script should exit with code 0.