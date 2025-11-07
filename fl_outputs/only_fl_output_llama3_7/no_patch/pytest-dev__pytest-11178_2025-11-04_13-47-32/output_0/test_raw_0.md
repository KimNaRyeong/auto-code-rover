Here is the reproducer script:

```python
import pytest
from functools import partial

def test_pytest_none_approx():
    actual_result = {"a": 1.2}
    expected_result = {"a": None}
    approx_expected_result = pytest.approx(expected_result, rel=0)
    assert approx_expected_result == actual_result

if __name__ == "__main__":
    try:
        test_pytest_none_approx()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.