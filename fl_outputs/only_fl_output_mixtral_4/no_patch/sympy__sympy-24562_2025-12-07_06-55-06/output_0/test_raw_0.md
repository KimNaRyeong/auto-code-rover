 Here's a standalone Python script `reproducer.py` that reproduces the issue:
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
    # Reproduce the issue
    issue_present = Rational('0.5', '100') != Rational(0.5, 100)

    # Check if the issue is present
    if issue_present:
        # Raise an AssertionError to indicate that the issue is present
        e = AssertionError("Rational calc value error")
        e.args += ("python 3.11, sympy 1.11.1",)
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```
To execute the script, run `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.