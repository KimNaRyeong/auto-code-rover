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

def t(func):
    return func

@t
def test_right_statement():
    foo = 1
    try:
        assert foo == (3 + 2) * (6 + 9), "Assertion failed"

        @t
        def inner():
            return 2

        assert 2 == inner, "Inner assertion failed"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1) # Exit with 1 to indicate failure when issue is present

    print("The issue seems to be fixed.")
    exit(0) # Exit with code 0 when issue is fixed

if __name__ == "__main__":
    test_right_statement()
