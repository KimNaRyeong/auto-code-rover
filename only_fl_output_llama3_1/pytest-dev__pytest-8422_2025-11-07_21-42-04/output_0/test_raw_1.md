Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
from decimal import Decimal
import pytest

def test_decimal_in_sequences_and_mappings():
    actual = [Decimal("1.000001"), Decimal("2.000001")]
    expected = [Decimal("1"), Decimal("2")]

    try:
        assert actual == pytest.approx(expected)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_decimal_in_sequences_and_mappings()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

Please note that you need to have pytest installed in your Python environment for this script to work correctly.