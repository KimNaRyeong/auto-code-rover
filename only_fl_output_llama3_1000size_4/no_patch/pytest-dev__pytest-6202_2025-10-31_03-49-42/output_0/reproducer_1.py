import pytest

def test_reproduce():
    a = '..['
    assert 0, f"Expected assertion error with headline '{a}'"

if __name__ == "__main__":
    try:
        test_reproduce()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed, exiting with code 0")
        exit(0)
