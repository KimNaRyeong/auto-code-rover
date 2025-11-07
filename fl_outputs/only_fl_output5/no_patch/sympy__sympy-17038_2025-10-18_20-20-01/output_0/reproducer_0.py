# reproducer.py
from sympy.core.power import isqrt

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

def verify_isqrt():
    test_cases = [
        {"n": 4503599761588224, "expected": 67108864},
        {"n": 9999999999999999, "expected": 99999999}
    ]

    for case in test_cases:
        n = case["n"]
        expected = case["expected"]
        result = isqrt(n)
        assert result == expected, f"isqrt({n}) = {result}, expected {expected}"

if __name__ == "__main__":
    try:
        verify_isqrt()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with non-zero code to indicate failure
    print("No issues detected.")
    exit(0)  # Exit with zero to indicate success
