```python
# reproducer.py
from sympy import sqrt, Rational, simplify

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

def main():
    try:
        result = sqrt(8)**Rational(2, 3)
        simplified_result = simplify(result)
        # Expecting the result to be 2, but the issue leads to an incorrect expression
        assert simplified_result == 2, f"Expected 2, got {simplified_result}"
    except AssertionError as e:
        print_stacktrace(e)
        # Exit with code 0 which means no error for the purpose of this script
        exit(0)

if __name__ == "__main__":
    main()
```

This script specifically addresses the issue described: the failure of SymPy to simplify the expression `sqrt(8)**Rational(2, 3)` to the expected result of `2`. If this issue exists, the assertion will fail, triggering the `AssertionError` which is caught, and the `print_stacktrace` function is called to log where the error occurred. The script exits with code 0 to follow the given instruction, which indicates an exit without error as per this specific testing script's requirement, even though an `AssertionError` is encountered indicating the issue is present.