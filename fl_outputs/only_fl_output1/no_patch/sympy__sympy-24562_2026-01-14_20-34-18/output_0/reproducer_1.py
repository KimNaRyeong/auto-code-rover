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

def test_rational_calculation_issue():
    from sympy import Rational, SympifyError

    # Attempt to create Rational number in two different ways that should be equivalent
    try:
        value1 = Rational('0.5', '100')
        expected = Rational(1, 200)
        assert value1 == expected, f"Rational('0.5', '100') evaluated to {value1}, expected {expected}"

        value2 = Rational(0.5, 100)
        assert value2 == expected, f"Rational(0.5, 100) evaluated to {value2}, expected {expected}"

    except AssertionError as e:
        print_stacktrace(e)
        raise  # Re-raise the AssertionError to make sure the script exits non-zero
    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        raise  # Re-raise to ensure proper exit code in case of unexpected error

if __name__ == "__main__":
    test_rational_calculation_issue()
    print("If this message is printed, the test did not find an issue, and it exited with code 0.")
