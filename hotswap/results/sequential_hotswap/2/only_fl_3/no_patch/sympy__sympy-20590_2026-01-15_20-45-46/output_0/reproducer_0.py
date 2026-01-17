import sympy

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

def verify_issue():
    try:
        # This line should raise an AttributeError in sympy version 1.6.2,
        # indicating that Symbol instances do not have a __dict__ attribute.
        dict_exists = hasattr(sympy.Symbol('s'), '__dict__')
        # If no AttributeError is caught, check if __dict__ exists and should not.
        assert dict_exists == False, "Symbol instances should not have a __dict__ attribute."
    except AssertionError as e:
        # If an AssertionError occurs, it means the issue is present.
        print_stacktrace(e)
        raise
    except Exception as e:
        # If any other exception is caught, the behavior is unexpected; print and raise.
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        verify_issue()
    except AssertionError:
        exit(1)  # Exit with code 1 if an AssertionError was raised indicating issue is present.
    exit(0)  # Exit with code 0 when no AssertionError, indicating issue is fixed or not reproducible.
