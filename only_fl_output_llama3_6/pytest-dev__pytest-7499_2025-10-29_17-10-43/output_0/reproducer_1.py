import pytest
from io import StringIO

def test_reproducer():
    msg = (
        f"Length of values ({29}) "
        f"does not match length of index ({30})"
    )
    with pytest.raises(AssertionError, match=msg):
        pass

if __name__ == "__main__":
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

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

