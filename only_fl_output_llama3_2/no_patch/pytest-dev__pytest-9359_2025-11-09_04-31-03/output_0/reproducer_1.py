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

def t(foo):
    return foo

@t
def outer():
    return 2

def test_right_statement():
    assert 1 == (3 + 2) * (6 + 9)
    @t
    def inner():
        return 2
    assert 2 == inner

try:
    test_right_statement()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
