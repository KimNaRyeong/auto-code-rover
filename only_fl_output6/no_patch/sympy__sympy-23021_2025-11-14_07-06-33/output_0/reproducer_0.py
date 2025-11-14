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

def test_decompogen_with_min_max():
    from sympy import Min, Symbol
    from sympy.solvers.decompogen import decompogen

    x = Symbol('x')
    try:
        result = decompogen(Min(5, x), x)
        # Before the fix, the following assertion would fail due to a RuntimeError
        # After the fix, it should pass, asserting that the issue is resolved
        assert result == [Min, 5, x], "decompogen failed to decompose Min/Max properly"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue with decompogen not handling Min/Max is present.")

if __name__ == "__main__":
    test_decompogen_with_min_max()
    print("The issue with decompogen not handling Min/Max is fixed.")
