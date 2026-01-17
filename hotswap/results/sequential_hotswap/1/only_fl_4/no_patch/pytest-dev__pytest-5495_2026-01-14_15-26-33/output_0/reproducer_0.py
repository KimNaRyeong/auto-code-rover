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

def test_comparisons():
    try:
        assert b"" == b"42"
    except AssertionError as e:
        print("Caught issue with byte string comparison 1:", file=sys.stderr)
        print_stacktrace(e)

    try:
        assert b"" == b"1"
    except AssertionError as e:
        print("Caught issue with byte string comparison 2:", file=sys.stderr)
        print_stacktrace(e)

if __name__ == "__main__":
    test_comparisons()
