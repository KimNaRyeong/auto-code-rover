import math
from sympy.core.power import isqrt

def test_isqrt():
    n = 4503599761588224
    s = isqrt(n)
    assert s == 67108864, f"Expected isqrt({n}) to be 67108864, but got {s}"
    assert s**2 <= n, f"isqrt({n}) is incorrect"

def test_isqrt_2():
    n = 9999999999999999
    s = isqrt(n)
    assert s == 99999999, f"Expected isqrt({n}) to be 99999999, but got {s}"

def main():
    try:
        test_isqrt()
        test_isqrt_2()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
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

    main()
