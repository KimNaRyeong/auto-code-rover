import sys

def simplify_expression():
    from sympy import Symbol, cos, simplify, I

    x = Symbol('x')
    try:
        # Attempt the expression that should trigger the issue.
        result = simplify(cos(x)**I)
        # If the operation succeeds without an error, it means the issue has been resolved.
        print("The operation completed successfully. The issue may have been fixed.")
        return True
    except Exception as e:
        # If an error occurs, the script will print the stacktrace and return False to indicate failure.
        print_stacktrace(e)
        return False

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

if __name__ == "__main__":
    if not simplify_expression():
        # If the function returns False, it means the issue is present. Raise an AssertionError.
        raise AssertionError("The issue is present.")
    # On successful completion without errors, exit with code 0 indicating no errors.
    sys.exit(0)
