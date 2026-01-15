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
    try:
        test_list_decimal()
        test_dict_decimal()
        print("Tests passed, the issue seems to be fixed.")
    except Exception:
        print("An issue occurred.",
              "The script should raise an AssertionError when the issue is present and print a stack trace of the issue.",
              "It should also exit with code 0 when the issue is fixed.", sep='\n')
        exit(1)
```