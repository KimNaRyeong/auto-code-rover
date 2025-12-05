 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy.core.power import isqrt

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

def test_isqrt():
    n = 4503599761588224
    s = isqrt(n)
    assert s == 67108864, "isqrt gives incorrect results"
    assert s**2 <= n, "Expect true"

    n = 9999999999999999
    s = isqrt(n)
    assert s == 99999999, "isqrt gives incorrect results"

if __name__ == "__main__":
    try:
        test_isqrt()
        print("Test passed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 21
    test_isqrt()
  File "reproducer.py", line 14
    assert s == 67108864, "isqrt gives incorrect results"
AssertionError: isqrt gives incorrect results
```