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

def test_simplification_issue():
    from sympy import symbols, I, sqrt, cos, pi, asinh, cosh, simplify

    # Original expression with the issue
    a = 2*sqrt(2)*I*cos(pi/6 - I*asinh(5*sqrt(2)/2)/3)/3
    a_simplified = simplify(a)

    # Correct simplified form of the expression
    correct_b = 2*sqrt(2)*I*cosh(I*pi/6 + asinh(5*sqrt(2)/2)/3)/3
    correct_b_simplified = simplify(correct_b)

    # Evaluating numerical values
    a_val = a.evalf()
    a_simplified_val = a_simplified.evalf()
    correct_b_simplified_val = correct_b_simplified.evalf()

    # Assert to verify if the issue exists
    try:
        assert a_val == a_simplified_val, "The original expressions did not simplify correctly."
        assert a_val == correct_b_simplified_val, "The corrected expressions did not simplify correctly."
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_simplification_issue()
    except Exception as e:
        # Ensure the script exits with code 1 if an exception occurs
        exit(1)
