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
    from sympy import symbols, Min, decompogen
    x = symbols('x')
    try:
        result = decompogen(Min(5, x), x)
        assert result == [Min, 5, x], "decompogen does not properly handle Min/Max"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("decompogen failed to handle Min/Max")

if __name__ == "__main__":
    test_decompogen_with_min_max()
    print("Test passed, issue is fixed.")
