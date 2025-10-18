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
