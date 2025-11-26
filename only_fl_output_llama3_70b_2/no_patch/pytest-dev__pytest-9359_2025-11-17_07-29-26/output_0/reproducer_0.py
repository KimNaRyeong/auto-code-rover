def t(foo):
    return foo

@t
def inner():
    return 2

def test_right_statement(foo):
    assert foo == (3 + 2) * (6 + 9)

    @t
    def outer():
        return 2

    assert 2 == outer()

try:
    foo = 1
    test_right_statement(foo)
except AssertionError as e:
    print_stacktrace(e)
