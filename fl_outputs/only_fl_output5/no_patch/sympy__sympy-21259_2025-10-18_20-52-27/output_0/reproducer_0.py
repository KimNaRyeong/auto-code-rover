from sympy import Range, Eq, Mod, floor, symbols

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

def test_issue():
    x = symbols('x')
    r = Range(3, 11, 2)
    expected = (x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1)
    try:
        assert r.as_relational(x) == expected
        print("Issue fixed, exiting with code 0.")
    except AssertionError as e:
        print("Assertion failed: Expected expression does not match the output from as_relational method.")
        print_stacktrace(e)
        raise SystemExit(1)

if __name__ == "__main__":
    test_issue()
