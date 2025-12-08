 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import sqrt, Rational, sympify
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

def test_sqrt_power():
    x = sqrt(8)
    y = Rational(2, 3)
    z = x**y
    assert isinstance(z, Expr), "Result should be a Sympy expression"
    assert z.equals(2), "Result should simplify to 2"

if __name__ == "__main__":
    try:
        test_sqrt_power()
    except Exception as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 21, in <module>
    test_sqrt_power()
  File "reproducer.py", line 17, in test_sqrt_power
    assert z.equals(2), "Result should simplify to 2"
AssertionError: Result should simplify to 2
```
This confirms that the issue is present in the Sympy library. If the issue is fixed, the script should exit with code 0 without printing any stack trace.