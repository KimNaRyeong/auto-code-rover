from sympy.core.power import isqrt
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_isqrt():
    n = 4503599761588224
    s = isqrt(n)
    assert s == 67108864, "Incorrect result for isqrt(n)"
    assert s**2 <= n, "Calculated square is greater than input"

if __name__ == "__main__":
    try:
        test_isqrt()
        print("Test passed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
