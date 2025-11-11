import pytest

def test_u():
    try:
        with pytest.raises(AssertionError, match=u"\u2603"):
            assert False, u"\u2603"
    except UnicodeEncodeError as e:
        print_stacktrace(e)
        exit(1)

try:
    test_u()
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
