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
    from sympy import S

    # Compare S(0.0) and S.false both ways.
    try:
        assert S(0.0) == S.false, "S(0.0) should be equal to S.false"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1) # Exit with an error code to indicate the first assertion failed.

    try:
        assert S.false == S(0.0), "S.false should be equal to S(0.0)"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1) # Exit with an error code to indicate the second assertion failed.

    # If neither of the above assertions fail, then the issue has been resolved.
    print("The issue has been fixed.")
    exit(0)

if __name__ == "__main__":
    main()
