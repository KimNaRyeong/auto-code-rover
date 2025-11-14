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

def reproduce_issue():
    from sympy import Rational

    # The problematic inputs as described in the issue
    rational_a = Rational('0.5', '100')
    rational_b = Rational(0.5, 100)

    # Checking the values against the expected outcomes
    assert rational_a == Rational(1,200), "Unexpected value for Rational('0.5', '100')"
    assert rational_b == Rational(1,200), "Unexpected value for Rational(0.5, 100)"

    print("All assertions passed. The issue is fixed or not present.")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero code to indicate failure due to the issue being present
