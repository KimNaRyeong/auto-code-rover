Here is the reproducer script:

```python
import pytest
from decimal import Decimal, getcontext

def test_decimal_in_sequences_and_mappings():
    getcontext().prec = 28  # Set precision to handle large decimals
    
    actual_list = [Decimal("1.000001"), Decimal("2.000001")]
    expected_list = [Decimal("1"), Decimal("2")]
    
    assert actual_list == pytest.approx(expected_list)
    
    actual_dict = {"a": Decimal("1.000001"), "b": Decimal("2.000001")}
    expected_dict = {"b": Decimal("2"), "a": Decimal("1")}
    
    assert actual_dict == pytest.approx(expected_dict)

if __name__ == "__main__":
    try:
        test_decimal_in_sequences_and_mappings()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Test passed.")
        exit(0)
```

This script will run the tests and raise an `AssertionError` if they fail, printing a stack trace of the issue. If the tests pass, it will print "Test passed." and exit with code 0.