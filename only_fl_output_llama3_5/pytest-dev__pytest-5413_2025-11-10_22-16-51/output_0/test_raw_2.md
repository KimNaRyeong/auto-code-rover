Here is the reproducer script:

```Python
def reproduce_issue():
    try:
        raise LookupError(
            f"A\n"
            f"B\n"
            f"C"
        )
    except LookupError as e:
        print(str(e))

    with pytest.raises(LookupError) as e:
        raise LookupError(
            f"A\n"
            f"B\n"
            f"C"
        )

    if str(e.value) != "A B C":
        print_stacktrace(e)
        assert False, "Expected the same error message"

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    reproduce_issue()
```

This script raises a `LookupError` in both cases and checks that the string representation of the exception is the same. If it's not, it prints the stack trace and asserts that an `AssertionError` should be raised.

Please note that you need to have pytest installed in your environment for this script to run correctly.