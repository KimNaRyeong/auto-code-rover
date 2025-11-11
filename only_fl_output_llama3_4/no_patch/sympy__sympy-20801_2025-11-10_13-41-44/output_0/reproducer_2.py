from sympy import S, false

def main():
    try:
        assert S(0.0) == S(false), "S(0.0) should be equal to S.false"
        print("Issue not reproduced")
    except AssertionError as e:
        print_stacktrace(e)
        raise

    try:
        if S(0.0) != S(false):
            raise AssertionError, "S(0.0) is not equal to S.false"
        if S(false) != S(0):
            raise AssertionError, "S.false is not equal to S(0)"
        if S(0) != S(false):
            raise AssertionError, "S(0) is not equal to S(false)"
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

if __name__ == "__main__":
    main()
