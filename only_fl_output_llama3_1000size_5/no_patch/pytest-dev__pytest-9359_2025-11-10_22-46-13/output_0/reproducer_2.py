def t(foo):
    return foo

@t
def inner():
    return 2

@t
def outer():
    return 2

def test_right_statement():
    assert (3 + 2) * (6 + 9) == 1
    assert inner() == 2
    assert outer() == 2

try:
    test_right_statement()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
