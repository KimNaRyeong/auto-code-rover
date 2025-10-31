import pytest

def test_reproducer():
    msg = (
        f"Length of values ({29}) "
        f"does not match length of index (30)"
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
        print("Test passed. No issue found.")
        exit(0)

