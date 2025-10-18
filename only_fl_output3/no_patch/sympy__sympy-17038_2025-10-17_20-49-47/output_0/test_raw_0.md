Here's a standalone Python script named `reproducer.py` that you can place in the root directory of the project. This script is designed to reproduce the issue as described, raising an `AssertionError` when the issue is present. It uses the `print_stacktrace` function to clearly show where the problem occurs if the assertion fails. When the issue is fixed, this script will exit with code 0 without any exceptions.

```python
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

def test_isqrt():
    from sympy.core.power import isqrt
    # Two test cases expected to fail based on the issue description
    test_cases = [(4503599761588224, 67108864), (9999999999999999, 99999999)]
    for n, expected in test_cases:
        try:
            result = isqrt(n)
            # Check both the expected result and the condition s**2 <= n
            assert result == expected, f"isqrt({n}) produced {result}, but {expected} was expected."
            assert result**2 <= n, f"Square of the result {result} for isqrt({n}) is not less than or equal to {n}."
        except AssertionError as e:
            print_stacktrace(e)
            exit(1)  # Exit with a failure code if any assertion fails

if __name__ == "__main__":
    test_isqrt()
    print("All tests passed successfully. No issue detected.")
    exit(0)
```

This script performs the followings steps:
- Defines the `print_stacktrace` function to display detailed information about where exceptions are raised.
- Defines the test function `test_isqrt` which checks the correctness of the `isqrt` function using two test cases that were previously shown to fail. It uses assertions to ensure that the output of `isqrt` matches the expected correct results and that the square of the calculated square root is indeed less than or equal to the input number.
- Executes the `test_isqrt` function when the script is run directly. If the issue is present, it will raise an `AssertionError` and the `print_stacktrace` function will output a detailed stack trace.
- If no exceptions are raised, the script prints a success message and exits with code 0, indicating that the issue could not be reproduced and hence, may have been fixed.

To run the script:
1. Make sure you have the reported versions of Python and SymPy installed.
2. Place the script in the root directory of your project.
3. Execute the script using `python3 reproducer.py`.