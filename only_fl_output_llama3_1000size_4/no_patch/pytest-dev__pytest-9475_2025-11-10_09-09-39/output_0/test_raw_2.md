Here is the reproducer script:

```python
import pytest
from _pytest.outcomes import Outcomes

def test_reproducer():
    result = pytest.main(["-k", "test_not_found_by_ini"])
    assert result.assert_outcomes(passed=2, deselected=0), print_stacktrace(AssertionError("Expected 2 passed outcomes and 0 deselected"))

if __name__ == "__main__":
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script runs the pytest command with the `-k` option to run only tests that match the pattern `test_not_found_by_ini`. It then asserts that there are 2 passed outcomes and 0 deselected. If the assertion fails, it prints a stack trace and exits with code 1.