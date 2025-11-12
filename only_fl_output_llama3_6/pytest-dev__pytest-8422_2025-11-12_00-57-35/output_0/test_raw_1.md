Here is the reproducer script:

```python
import decimal

def test_approx_decimal():
    actual = [decimal.Decimal("1.000001"), decimal.Decimal("2.000001")]
    expected = [decimal.Decimal("1"), decimal.Decimal("2")]

    assert actual == pytest.approx(expected)

print_stacktrace(AssertionError)
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.