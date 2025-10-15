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

def main():
    from sympy import symbols, cos, pi, I, sqrt, asinh, simplify

    # Original expression
    a = 2*sqrt(2)*I*cos(pi/6 - I*asinh(5*sqrt(2)/2)/3)/3
    # Simplified expression
    b = simplify(a)

    # Evaluate both expressions numerically
    a_val = a.evalf()
    b_val = b.evalf()

    # Check if the numerical values are equal
    try:
        assert a_val == b_val, "Numerical values of `a` and `b` are not equal."
    except AssertionError as e:
        print("AssertionError encountered, indicating the issue is present.")
        print_stacktrace(e)
        raise SystemExit(1) from None
    else:
        print("No AssertionError, the issue seems to be fixed.")

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print("An unexpected error occurred.")
        print_stacktrace(e)
        raise SystemExit(1) from None
    else:
        SystemExit(0)
