Here is the reproducer script:

```python
import pytest

def test_reproducer():
    result = pytest.runpytest("-k", "test_not_found_by_ini")
    assert result.assert_outcomes(passed=2), print_stacktrace(AssertionError("Expected 2 passed outcomes"))

if __name__ == "__main__":
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script uses the `pytest.runpytest()` function to run a pytest session with the `-k` option, which runs only tests matching the given keyword. The script then asserts that the number of passed outcomes is 2, which should raise an `AssertionError` if the issue is present.

Please note that this reproducer script assumes that you have pytest installed in your environment and available for use.