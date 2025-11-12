Here is the reproducer script:

```python
import pytest
from decimal import Decimal

def test_approx_decimal():
    within_1e6 = [
        (Decimal("1.000001"), Decimal("1.0")),
        (Decimal("-1.000001"), Decimal("-1.0")),
    ]
    for a, x in within_1e6:
        assert a == pytest.approx(x)

def test_approx_list_decimal():
    actual = [Decimal("1.000001"), Decimal("2.000001")]
    expected = [Decimal("1"), Decimal("2")]

    with pytest.raises(AssertionError):
        assert actual == pytest.approx(expected)

def test_approx_dict_decimal():
    actual = {"a": Decimal("1.000001"), "b": Decimal("2.000001")}
    expected = {"b": Decimal("2"), "a": Decimal("1")}

    with pytest.raises(AssertionError):
        assert actual == pytest.approx(expected)

if __name__ == "__main__":
    try:
        test_approx_decimal()
        test_approx_list_decimal()
        test_approx_dict_decimal()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.