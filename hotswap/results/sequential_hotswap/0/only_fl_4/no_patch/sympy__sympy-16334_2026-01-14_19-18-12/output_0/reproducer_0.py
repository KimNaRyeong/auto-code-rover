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
    from sympy import symbols, ask, Q
    from sympy.abc import x, y, z

    p = symbols('p', real=True, zero=False)
    q = symbols('q', zero=True)
    result = (q**p).is_positive
    # Since 0**a (where a is real and non-zero) should be interpreted as either 0 or undefined (zoo in sympy),
    # the expression should not evaluate as positive.
    assert result is False, f"Expected (q**p).is_positive to be False, got {result}"

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    else:
        print("Test passed: the issue does not exist.")
