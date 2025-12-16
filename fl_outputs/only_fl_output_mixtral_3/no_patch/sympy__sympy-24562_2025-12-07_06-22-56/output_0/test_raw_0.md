 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback
from sympy import Rational

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        # The issue is present in sympy version 1.11.1
        # when calc Rational('0.5', '100'), the value is 1/100100
        assert Rational('0.5', '100') == 1/100100, "The value is not 1/100100"

        # Rational(0.5, 100) the value is 1/200, this value is the true value
        assert Rational(0.5, 100) == 1/200, "The value is not 1/200"

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace, indicating that the issue is present. When the issue is fixed, the script should exit with code 0.