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

def test_isqrt_correctness():
    from sympy.core.power import isqrt

    # Two test cases where isqrt is known to fail in the reported issue.
    test_cases = [
        (4503599761588224, 67108864),
        (9999999999999999, 99999999)
    ]

    for n, expected in test_cases:
        result = isqrt(n)
        # Check the correctness of the result
        correct_result = result == expected
        # Check if the square of the result is less than or equal to n
        square_condition = result**2 <= n
        try:
            assert correct_result and square_condition
        except AssertionError as e:
            print(f"Assertion failed for isqrt({n}):")
            print(f"Expected {expected}, got {result}")
            print(f"Is square less than or equal to n? {square_condition}")
            print_stacktrace(e)
            # Exit on the first failure
            exit(1)

if __name__ == "__main__":
    test_isqrt_correctness()
    print("All tests passed successfully.")
```

This Python script will test the correctness of the `isqrt` function for the specified inputs and compare the results with the expected correct values. If the function returns an incorrect result or fails the square condition, the script will raise an `AssertionError`, print a detailed stack trace, and exit with a non-zero status code. If the function passes all tests, the script will print a success message and exit with code 0.