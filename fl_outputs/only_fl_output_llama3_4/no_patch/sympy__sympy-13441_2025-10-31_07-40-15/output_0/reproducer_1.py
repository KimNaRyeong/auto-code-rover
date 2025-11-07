def your_function():
    assert 1 == 2, "This should not be executed"
    return "expected_result"

try:
    result = your_function()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print(result)
exit(0)
