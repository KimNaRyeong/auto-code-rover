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
    x = symbols('x')
    f = Function('f')

    # Reproduce the issue
    expr1 = x + cos(x)
    expr2 = exp(x) + cos(x)

    # expr1.subs(x, oo) should be oo, but it's not
    try:
        res1 = expr1.subs(x, oo)
        assert res1 == oo
    except AssertionError as e:
        print_stacktrace(e)
        return 1

    # expr2.subs(x, oo) should be AccumBounds, but it's not
    try:
        res2 = expr2.subs(x, oo)
        assert res2 == exp(oo) + cos(oo)
    except AssertionError as e:
        print_stacktrace(e)
        return 1

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
```
When executed, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    sys.exit(main())
  File "reproducer.py", line 24, in main
    assert res1 == oo
AssertionError:
```
This indicates that the issue is present, as `expr1.subs(x, oo)` does not evaluate to `oo`.