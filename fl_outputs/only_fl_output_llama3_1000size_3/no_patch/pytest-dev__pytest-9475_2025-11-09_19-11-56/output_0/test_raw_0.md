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

This script uses the `pytest.main()` function to run a pytest session with the `-k` option, which runs only tests matching the given keyword. The script then asserts that the number of passed outcomes is 2, which should raise an `AssertionError` if the issue is present.