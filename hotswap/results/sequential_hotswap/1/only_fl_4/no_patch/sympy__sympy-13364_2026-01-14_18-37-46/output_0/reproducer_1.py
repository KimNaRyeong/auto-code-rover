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

def test_ternary_pow():
    from sympy import S
    try:
        # Using Python's built-in pow function with SymPy's symbolic objects
        result = pow(S(2), S(3), S(5))
        # If the issue is present, TypeError or a similar exception might be raised before this assertion
        assert result == S(3), "Expected 2 ** 3 % 5 == 3"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to support ternary pow() with sympy.S objects.") from e

if __name__ == "__main__":
    test_ternary_pow()
