import sympy
from sympy import symbols, Range, Eq, Mod, floor

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

def check_as_relational():
    x = symbols('x')
    range_obj = Range(3, 11, 2)
    expected_relational = (x >= 3) & (x <= 9) & Eq(x, floor(x)) & Eq(Mod(x, 2), 1)
    calculated_relational = range_obj.as_relational(x)
    # The assertion checks if the condition accurately represents the range steps and start value
    assert calculated_relational == expected_relational, "The generated relational representation is incorrect."

if __name__ == "__main__":
    try:
        check_as_relational()
        print("No issues found. The issue is likely fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with nonzero code to indicate failure/assertion error status
    except Exception as e:  # Catching any other unexpected errors
        print_stacktrace(e)
