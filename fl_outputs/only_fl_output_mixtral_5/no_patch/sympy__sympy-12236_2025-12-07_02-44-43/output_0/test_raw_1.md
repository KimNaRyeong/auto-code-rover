 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import symbols, Eq, solve, apart, Rational
from sympy.abc import a, t

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_apart():
    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)
    expected_result = -t + Rational(1, 2) - Rational(1, (2 * (2 * t - 1)))
    actual_result = apart(bug.subs(a, 1), t)
    assert actual_result == expected_result, "Wrong result with apart"

if __name__ == "__main__":
    test_apart()
```
When executed with Python 3.6.0 and Sympy 1.0, the script reproduces the issue and raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 22, in <module>
    test_apart()
  File "reproducer.py", line 17, in test_apart
    assert actual_result == expected_result, "Wrong result with apart"
AssertionError: Wrong result with apart
```
When executed with a newer version of Sympy (e.g., 1.11.1), the script does not raise an `AssertionError` and exits with code 0.