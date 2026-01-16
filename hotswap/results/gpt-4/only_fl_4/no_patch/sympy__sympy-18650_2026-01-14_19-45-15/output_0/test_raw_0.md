```python
# reproducer.py
from sympy import sqrt, Rational

def assert_issue():
    # Attempting to reproduce the issue where sqrt(8)**Rational(2, 3) doesn't simplify to 2
    result = sqrt(8)**Rational(2, 3)
    expected = 2
    # Asserting the simplification equals 2, to confirm the issue. 
    assert result == expected, f"Expected {expected}, got {result}"

if __name__ == "__main__":
    try:
        assert_issue()
    except AssertionError as e:
        def print_stacktrace(e: Exception):
            import traceback
            import sys
            tb = traceback.extract_tb(e.__traceback__)
            print("Traceback (most recent call last):", file=sys.stderr)
            for frame in tb:
                line_number = frame.lineno
                code_context = frame.line.strip() if frame.line else "Unknown"
                print(f'  File "{frame.filename}"', file=sys.stderr)
                print(f"    {line_number}: {code_context}", file=sys.stderr)
            print(f"{e.__class__.__name__}: {e}", file=sys.stderr)
        
        print_stacktrace(e)
        raise SystemExit(1)  # Indicate failure by non-zero exit
    else:
        print("No issues detected.")
```

This script checks for the issue where `sqrt(8)**Rational(2, 3)` does not simplify to `2`. It uses an assertion to confirm if the problem exists. If the issue is present, the script raises an `AssertionError`, and a stack trace is printed to provide more information on where the issue occurred. If the issue is not present (which means the assertion passed), the script prints "No issues detected." and exits with code 0, indicating success.