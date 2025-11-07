Here is the reproducer script:

```python
import fractions
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        x = 0
        assert x not in fractions.Fraction(1/x)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script uses the `Fraction` class from Python's standard library to create a fraction with a denominator of 0. It then attempts to check if `x` is not in this fraction using an assertion statement. If the assertion fails, it prints the stack trace and then re-raises the exception.