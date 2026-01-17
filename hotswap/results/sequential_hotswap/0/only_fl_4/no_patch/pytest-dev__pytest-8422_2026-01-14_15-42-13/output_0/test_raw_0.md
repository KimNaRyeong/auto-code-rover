```python
# reproducer.py
from decimal import Decimal
from pytest import approx

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

def test_list_decimal():
    actual = [Decimal("1.000001"), Decimal("2.000001")]
    expected = [Decimal("1"), Decimal("2")]

    try:
        assert actual == approx(expected)
    except Exception as e:
        print_stacktrace(e)
        raise

def test_dict_decimal():
    actual = {"a": Decimal("1.000001"), "b": Decimal("2.000001")}
    expected = {"b": Decimal("2"), "a": Decimal("1")}

    try:
        assert actual == approx(expected)
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_list_decimal()
    test_dict_decimal()
    print("Tests passed successfully!")
```

This standalone Python script `reproducer.py` is designed to reproduce the issue described. When executed, it attempts to use `pytest`'s `approx` function to assert the equality of lists and dictionaries containing `Decimal` values, which according to the issue description, raises a `TypeError`.

- When the issue is present, this script will catch the exception, print the stack trace using the provided `print_stacktrace` function to clearly show where the problem occurs, and then re-raise the exception to exit with a non-zero status code due to the `AssertionError`.
- Once the issue is fixed, the assertions should pass, and the script will print "Tests passed successfully!" and exit with code 0.