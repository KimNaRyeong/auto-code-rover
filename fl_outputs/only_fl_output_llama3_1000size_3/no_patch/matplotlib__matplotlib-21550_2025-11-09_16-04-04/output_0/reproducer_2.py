def your_function():
    assert 1 == 2, "This assertion should fail"
    return "Hello"

print_stacktrace(AssertionError("This assertion should fail"))

if __name__ == '__main__':
    print(your_function())
