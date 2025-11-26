import decimal
import pytest

def approx(a, rel=1e-6, abs=0):
    return pytest.approx(a, rel=rel, abs=abs)

def test_list_decimal():
    actual = [decimal.Decimal("1.000001"), decimal.Decimal("2.000001")]
    expected = [decimal.Decimal("1"), decimal.Decimal("2")]

    try:
        assert actual == approx(expected)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Test failed")

def test_dict_decimal():
    actual = {"a": decimal.Decimal("1.000001"), "b": decimal.Decimal("2.000001")}
    expected = {"b": decimal.Decimal("2"), "a": decimal.Decimal("1")}

    try:
        assert actual == approx(expected)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Test failed")

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

test_list_decimal()
test_dict_decimal()

print("All tests passed")
