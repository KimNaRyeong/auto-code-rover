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

def test_is_number_on_undefined_function():
    from sympy import Function, symbols

    # Create an undefined function with a number argument
    f = Function('f')
    x = symbols('x')
    expr = f(1)

    # Check if `is_number` returns `False` for an undefined function with a number argument
    try:
        assert expr.is_number == False, "is_number should be False for undefined functions with number arguments."
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with a non-zero exit code to indicate failure

    # If we reach this point, it means the issue is fixed.
    print("The issue has been fixed.")
    exit(0)

if __name__ == "__main__":
    test_is_number_on_undefined_function()
