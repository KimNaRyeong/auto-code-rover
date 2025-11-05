def main():
    try:
        settings.configure(types.SimpleNamespace(foo="bar"), baz="qux")
        print_stacktrace(AssertionError("Expected AssertionError not to be raised."))
    except Exception as e:
        print_stacktrace(e)
        exit(0)

print_stacktrace(AssertionError("Expected AssertionError not to be raised."))

if __name__ == "__main__":
    main()
