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

def test_piecewise_rewrite_for_min_max():
    from sympy import Max, Symbol, Piecewise
    a = Symbol('a')
    b = Symbol('b')

    try:
        result = Max(a, b).rewrite(Piecewise)
        expected = Piecewise((a, a>b), (b, True))
        # Verify the result matches the expected outcome
        assert result == expected, f"Expected {expected} but got {result}"
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_piecewise_rewrite_for_min_max()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    print("No issues detected.")
    exit(0)
