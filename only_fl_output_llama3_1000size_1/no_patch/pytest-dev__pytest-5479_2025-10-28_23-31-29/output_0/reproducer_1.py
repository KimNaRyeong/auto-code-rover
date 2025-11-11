import pytest
from io import StringIO

def test_u():
    f = StringIO(u"\u2603")
    try:
        assert False, f.getvalue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_u()
