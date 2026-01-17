from sympy import Function, symbols
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_undefined_function_number_argument():
    """
    Check if an undefined function with a number argument has is_number=False.
    """
    f = Function('f')
    x = symbols('x')
    try:
        # Assertion to check if the behavior is as expected
        assert not f(1).is_number, "Undefined function with number argument should not have is_number=True"
    except AssertionError as e:
        print_stacktrace(e)  # Print the stack trace if the assertion fails
        exit(1)  # Exit with error status if the issue is present
    else:
        print("Test passed: The issue has been fixed.")  # Indicate the issue has been resolved if no assertion fails

if __name__ == "__main__":
    test_undefined_function_number_argument()
    exit(0)  # Exit with success status if the issue is fixed
