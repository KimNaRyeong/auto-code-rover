from sympy import S

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

def check_assertion():
    # This assertion checks whether S(0.0) == S.false evaluates to False, which is inconsistent
    assert S(0.0) == S.false, "S(0.0) == S.false should return False according to the expectation."

    # This assertion checks the consistency of S.false == S(0.0)
    assert S.false == S(0.0), "S.false == S(0.0) should return True to be consistent."

if __name__ == "__main__":
    try:
        check_assertion()
        print("No issue detected.")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
