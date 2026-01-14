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

    test_cases = [
        (4503599761588224, 67108864),
        (9999999999999999, 99999999),
    ]

    for n, expected in test_cases:
        s = isqrt(n)
        assert s == expected, f"Expected {expected}, got {s} for isqrt({n})"
        assert s**2 <= n, f"Result of isqrt({n}) squared should be <= {n}"

if __name__ == "__main__":
    try:
        test_isqrt()
        print("No issues detected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
