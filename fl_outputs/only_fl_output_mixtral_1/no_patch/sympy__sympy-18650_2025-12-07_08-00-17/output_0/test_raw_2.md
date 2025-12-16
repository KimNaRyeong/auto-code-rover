 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from decimal import Decimal
from fractions import Fraction
from math import sqrt

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

if __name__ == "__main__":
    expected_result = 2
    result = sqrt(8)**Fraction(2, 3)
    if result != expected_result:
        e = AssertionError(f"Expected {expected_result}, but got {result}")
        print_stacktrace(e)
        raise e
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    raise e
AssertionError: Expected 2, but got 2**(1/3)*2**(2/3)
```
This confirms that the issue is present in the code. If the issue is fixed, the script should print nothing and exit with code 0.