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
    # Reproduce the issue
    issue_present = Rational('0.5', '100') != Rational(0.5, 100)

    # Check if the issue is present
    if issue_present:
        # Raise an AssertionError to indicate that the issue is present
        e = AssertionError("Rational value error: 0.5/100 != 0.5/100")
        print_stacktrace(e)
        sys.exit(1)
    else:
        # Exit with code 0 to indicate that the issue is fixed
        sys.exit(0)

if __name__ == "__main__":
    main()
```
To run the script, execute the following command in the root directory of the project:
```
python3 reproducer.py
```
If the issue is present, the script will raise an `AssertionError` and print a stack trace. If the issue is fixed, the script will exit with code 0.