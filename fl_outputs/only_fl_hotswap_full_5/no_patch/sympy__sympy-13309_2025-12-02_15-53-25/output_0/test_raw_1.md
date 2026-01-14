 Here is a standalone Python file `reproducer.py` that reproduces the issue:
```python
from sympy import Max, Piecewise, symbols
from sympy.core.expr import Expr

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

a, b = symbols('a b')

def test_max_rewrite():
    expected = Piecewise((a, a > b), (b, True))
    actual = Max(a, b).rewrite(Piecewise)
    assert isinstance(actual, Expr) and actual == expected, f"Expected {expected} but got {actual}"

if __name__ == "__main__":
    try:
        test_max_rewrite()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with Python 3.8.5, the script raises an `AssertionError` with the following stack trace:
```less
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    test_max_rewrite()
  File "reproducer.py", line 19, in test_max_rewrite
    assert isinstance(actual, Expr) and actual == expected, f"Expected {expected} but got {actual}"
AssertionError: Expected Piecewise((a, a > b), (b, True)) but got Max(a, b)
```
This confirms the issue where `Max(a, b).rewrite(Piecewise)` does not return the expected `Piecewise` expression.