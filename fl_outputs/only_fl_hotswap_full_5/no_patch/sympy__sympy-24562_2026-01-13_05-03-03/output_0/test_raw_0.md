 Here is a standalone python file `reproducer.py` to reproduce the issue:

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
        # The issue is present when the value is 1/100100
        value1 = Rational('0.5', '100')
        assert value1 == Rational(0.5, 100), "The value is not equal to 1/200"

        # The issue is fixed when the value is 1/200
        # value2 = Rational('0.5', '100')
        # assert value2 == Rational(0.5, 100), "The value is not equal to 1/200"

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace with the line numbers of the statements. The script should exit with code 1 when the issue is present.

When the issue is fixed, you can uncomment the second set of statements and the script should exit with code 0.