Here is the reproducer script:

```python
import pytest
from _pytest.outcomes import Outcomes

def test_reproducer():
    result = pytest.main(["-k", "test_not_found_by_ini"])
    assert Outcomes.passed == 2, print_stacktrace(AssertionError)

if __name__ == "__main__":
    try:
        test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script runs the pytest command with the `-k` option to run tests that match the pattern `test_not_found_by_ini`. It then asserts that the number of passed outcomes is 2. If this assertion fails, it prints a stack trace and exits with code 1. If the assertion passes, it exits with code 0.

You can put this script in a file named `reproducer.py` and run it using `python3 reproducer.py`.