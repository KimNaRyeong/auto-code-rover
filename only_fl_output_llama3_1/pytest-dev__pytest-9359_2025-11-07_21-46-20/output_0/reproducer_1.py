def t(foo):
    return foo

def test_right_statement():
    assert 1 == (3 + 2) * (6 + 9)

    @t
    def inner():
        return 2

    print_stacktrace(AssertionError("1 != 75"))

if __name__ == "__main__":
    try:
        test_right_statement()
    except Exception as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
