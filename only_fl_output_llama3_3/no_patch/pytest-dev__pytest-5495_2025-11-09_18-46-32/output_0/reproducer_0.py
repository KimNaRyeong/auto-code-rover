def test_b():
    assert b"" == b"42"

try:
    test_b()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present, exiting with code 0")
exit(0)
