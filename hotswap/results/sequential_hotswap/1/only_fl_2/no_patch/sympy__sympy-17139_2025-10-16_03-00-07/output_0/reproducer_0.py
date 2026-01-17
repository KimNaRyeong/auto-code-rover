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

def test_simplify_cos_i():
    from sympy import Symbol, cos, simplify
    x = Symbol('x')
    try:
        result = simplify(cos(x)**I)
        # The operation should raise an Exception for the issue
        # If it succeeds, then the issue is presumed to be fixed
        print("Issue seems to be resolved, exiting with code 0")
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        assert isinstance(e, TypeError), "Expected TypeError, got different exception"
        assert "Invalid comparison of complex I" in str(e), "Expected specific error message, got different message"

if __name__ == "__main__":
    test_simplify_cos_i()
