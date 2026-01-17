```python
from sympy import symbols, Subs
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    x, y, a, z = symbols('x y a z')
    initial_subs = Subs(x + y, (a,), (4,))
    result1 = initial_subs.subs(a,z)
    expected1 = Subs(x + y, (a,), (4,))

    if result1 != expected1:
        raise AssertionError("First substitution did not yield the expected result.")

    intermediate_subs = Subs(x + y, (a,), (a,))
    result2 = intermediate_subs.subs(a, z)
    expected2 = Subs(x + y, (a,), (z,))

    # This is where the issue is expected to occur
    if result2 != expected2:
        raise AssertionError("Second substitution did not yield the expected result.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    print("No issues detected.")
```

This script will attempt to reproduce the substitution issue as described. It first makes a substitution that is expected to work as intended, and then it tries a second substitution where the issue is anticipated. If the issue arises (meaning the second substitution does not behave as expected), it will raise an `AssertionError` and print a detailed stack trace using the provided `print_stacktrace` function. The script exits with code 0 if no issues are found, indicating the problem has been fixed, or with code 1 if an error is caught, indicating the presence of the issue.