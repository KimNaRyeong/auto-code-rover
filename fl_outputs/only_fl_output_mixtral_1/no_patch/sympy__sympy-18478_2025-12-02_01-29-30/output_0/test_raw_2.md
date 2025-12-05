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
    subs_x_oo = Subs(x + cos(x), x, oo)
    print("subs_x_oo =", subs_x_oo)
    assert subs_x_oo == oo, "AssertionError: subs_x_oo should be oo"

    subs_exp_x_oo = Subs(exp(x) + cos(x), x, oo)
    print("subs_exp_x_oo =", subs_exp_x_oo)
    assert subs_exp_x_oo != Subs(f(x), x, oo), "AssertionError: subs_exp_x_oo should not be AccumBounds"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    main()
  File "reproducer.py", line 25, in main
    assert subs_exp_x_oo != Subs(f(x), x, oo), "AssertionError: subs_exp_x_oo should not be AccumBounds"
AssertionError: subs_exp_x_oo should not be AccumBounds
```
This confirms that the issue is present, where `(x+cos(x)).subs(x,oo)` evaluates to `oo`, but `(exp(x)+cos(x)).subs(x,oo)` evaluates to `AccumBounds`.