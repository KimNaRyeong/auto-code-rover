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

def test_expand_trig_issue():
    from sympy import symbols, expand_trig, tanh, csch, sech, sin, cos, csc, sec

    x, y = symbols('x y')
    try:
        # Validate expected expansions
        assert expand_trig(tanh(x + y)) == (tanh(x) + tanh(y))/(tanh(x)*tanh(y) + 1)

        # Currently not expanding as expected, these two should raise AssertionError
        assert expand_trig(csch(x + y)) != csch(x + y), "csch(x + y) not expanded"
        assert expand_trig(sech(x + y)) != sech(x + y), "sech(x + y) not expanded"

        # Reference for correct expansions
        assert expand_trig(csc(x + y)) == 1/(sin(x)*cos(y) + sin(y)*cos(x))
        assert expand_trig(sec(x + y)) == 1/(-sin(x)*sin(y) + cos(x)*cos(y))
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_expand_trig_issue()
    print("Issue is fixed, exiting with code 0.")
    exit(0)
