import pytest
import sys

def test_u():
    try:
        with pytest.raises(AssertionError, match=u"\u2603"):
            assert False, u"\u2603"
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_u()
