def test_b():
    assert b"" == b"1"

if __name__ == "__main__":
    try:
        test_b()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
