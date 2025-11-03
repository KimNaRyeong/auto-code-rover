def your_function():
    assert 1 == 2, "This should never happen"
    return "Hello"

try:
    result = your_function()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print(result)
exit(0)
