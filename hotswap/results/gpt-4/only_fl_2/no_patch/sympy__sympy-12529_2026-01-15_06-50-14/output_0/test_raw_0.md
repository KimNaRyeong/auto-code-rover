```python
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

def main():
    from sympy import totient

    try:
        # Attempt to calculate the totient of a non-integer (2.3),
        # which is not defined according to the Totient function definition.
        result = totient(2.3)
        # An error should be raised for non-integer input; if not, assert failure.
        assert isinstance(result, TypeError), "Expected a TypeError for non-integer input."
    except Exception as e:
        print_stacktrace(e)
        # Raise the AssertionError to indicate the issue is present.
        raise AssertionError("The Totient function should not accept non-integer numbers.") from e

if __name__ == "__main__":
    main()
```

This script attempts to use the `totient` function from SymPy on a non-integer number, which is not supposed to be valid input for the Totient function according to mathematical definitions. The script should raise an `AssertionError` if the issue (accepting non-integer inputs without error) is present. It uses a custom function `print_stacktrace` to print the stack trace in a clear format as required.