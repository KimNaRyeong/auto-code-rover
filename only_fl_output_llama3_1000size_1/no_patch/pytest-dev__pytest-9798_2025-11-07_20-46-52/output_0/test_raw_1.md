Here is the reproducer script:

```python
import pytest
from _pytest.python_api import approx

def test_approx():
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_approx()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.