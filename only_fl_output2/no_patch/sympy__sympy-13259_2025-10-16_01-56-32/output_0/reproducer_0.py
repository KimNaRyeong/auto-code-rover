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
    from sympy import I, asinh, cos, pi, sqrt, S
    try:
        # Defining the initial expression
        a = 2 * sqrt(2) * I * cos(pi / 6 - I * asinh(5 * sqrt(2) / 2) / 3) / 3
        a_evaluated = a.evalf()

        # Simplified expression
        b = a.simplify()
        b_evaluated = b.evalf()

        # The assertion checks if the simplified expression `b` equals `a` numerically
        assert a_evaluated == b_evaluated, "The simplified expression does not match the original numerically."

        print("Issue is fixed.")  # If no error occurs, the issue is fixed.
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with error status if the issue is reproduced.

if __name__ == "__main__":
    main()
