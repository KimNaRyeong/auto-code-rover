Here is the reproducer script:

```python
import pytest
from _pytest.outcomes import Outcomes

def test_reproducer():
    result = pytest.main(["-k", "test_not_found_by_ini"])
    assert Outcomes.passed == 2, print_stacktrace(AssertionError("Expected 2 passed outcomes"))

if __name__ == "__main__":
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script runs the pytest command with the `-k` option to run only tests that match the pattern `test_not_found_by_ini`. It then asserts that there are 2 passed outcomes. If the assertion fails, it prints a stack trace and exits with code 1.