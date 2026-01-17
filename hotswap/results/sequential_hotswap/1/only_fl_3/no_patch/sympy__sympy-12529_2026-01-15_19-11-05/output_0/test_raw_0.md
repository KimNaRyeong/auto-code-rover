```python
# reproducer.py
from sympy import totient

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

def test_totient_non_integer_input():
    try:
        result = totient(2.3)
        # An error should be raised for non-integer input; if it's not, we assert False to indicate the issue.
        assert result == "Error", "Totient function didn't raise error on non-integer input as expected."
    except Exception as e:
        print_stacktrace(e)
        # Reraising the exception so the program exits with a non-zero code if the issue is present.
        raise

if __name__ == "__main__":
    try:
        test_totient_non_integer_input()
        # If the test passes without exceptions, we suspect the issue is fixed and exit cleanly.
        print("No issue detected.")
    except AssertionError:
        # This block will execute if an AssertionError was raised, indicating the issue was detected.
        # Exiting with code 0 to comply with the requirement for this specific scenario.
        import sys
        sys.exit(0)
```