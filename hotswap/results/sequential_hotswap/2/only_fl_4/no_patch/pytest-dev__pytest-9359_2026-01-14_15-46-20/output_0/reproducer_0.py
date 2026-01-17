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

def test_right_statement():
    foo = 1
    try:
        assert foo == (3 + 2) * (6 + 9)

        @t
        def inner():
            return 2

        assert 2 == inner
    except AssertionError as e:
        print_stacktrace(e)
        # Exiting with code 0 to signal that the reproducer has completed as expected.
        # In a real scenario, you might handle this differently depending on the context and requirements.
        sys.exit(0)

if __name__ == "__main__":
    test_right_statement()
