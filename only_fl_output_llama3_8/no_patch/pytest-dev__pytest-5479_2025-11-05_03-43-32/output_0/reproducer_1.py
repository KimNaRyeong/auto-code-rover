from unittest.mock import patch

def test_u():
    try:
        assert False, u"\u2603"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_u()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
