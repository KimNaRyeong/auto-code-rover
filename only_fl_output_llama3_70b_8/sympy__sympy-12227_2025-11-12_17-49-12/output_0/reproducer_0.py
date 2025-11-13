import sympy

def test_float_constructor():
    try:
        # Try to create a Float with 54 binary digits
        f = sympy.Float(1.0, prec=54)
        assert False, "Expected ValueError or TypeError"
    except (ValueError, TypeError):
        pass  # Expected behavior

    try:
        # Check if setting decimal precision works
        f = sympy.Float(1.0, 15)
        assert f._prec != 54, "Decimal precision did not convert correctly to binary precision"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

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

if __name__ == "__main__":
    test_float_constructor()
