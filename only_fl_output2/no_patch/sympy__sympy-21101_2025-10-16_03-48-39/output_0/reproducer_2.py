# reproducer.py

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
    from sympy import Mul, S, latex
    # Attempt to generate latex representation with unevaluated Mul
    result = latex(Mul(6, S.Half, evaluate=False))
    # The expected latex should include a separator (e.g., '\cdot') between terms
    expected = "6 \\cdot \\frac{1}{2}"
    
    # Adjust the expected result according to the actual issue specifics
    incorrect_result = "6 1/2"
    assert result != incorrect_result, f"Issue reproduced: Expected not {incorrect_result}, got {result}"
    assert result == expected, f"Incorrect latex representation: Expected {expected}, got {result}"

if __name__ == "__main__":
    try:
        test_issue()
        print("The test did not reproduce the issue. Exiting with code 0.")
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)
    except Exception as e:
        print_stacktrace(e)
        raise SystemExit(1)
