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
    import sympy

    s0 = sympy.Symbol('s0')
    try:
        result = sympy.Integer(1024) // s0
        # If we reach here without an exception, the issue is considered fixed.
        print("Issue is fixed. Exiting with code 0.")
        exit(0)
    except Exception as e:
        # If we are seeing the specific TypeError, it means the issue still exists.
        if "Argument of Integer should be of numeric type" in str(e):
            print_stacktrace(e)
            raise AssertionError("The issue with sympy.Integer floor division is still present.")
        else:
            # If there's any other exception, raise it as this script is focused on the specific issue.
            raise

if __name__ == "__main__":
    main()
