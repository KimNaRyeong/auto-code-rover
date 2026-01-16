```python
# reproducer.py
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
    from sympy import sqrt, Rational
    try:
        # Here is where we reproduce the reported issue
        result = sqrt(8)**Rational(2, 3)
        expected_result = 2

        # Simplify the result if not already simplified. This is a workaround for checking equality.
        simplified_result = result.simplify()
        # Raise an AssertionError if the issue is present
        assert simplified_result == expected_result, f"Expected {expected_result}, got {simplified_result}"
    except Exception as e:
        print_stacktrace(e)

# Running the main function
if __name__ == "__main__":
    main()
```