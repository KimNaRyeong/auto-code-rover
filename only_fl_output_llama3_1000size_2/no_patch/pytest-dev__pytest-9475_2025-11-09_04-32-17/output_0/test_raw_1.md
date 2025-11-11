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

This script runs pytest with the `-k` option to run only tests matching the given keyword, and then asserts that the number of passed outcomes is 2. If this assertion fails, it prints the stack trace and exits with code 1.