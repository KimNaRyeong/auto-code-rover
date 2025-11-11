Here is the reproducer script:

```python
import pytest
from _pytest.python_api import approx

def test_approx():
    assert [1, 2] == approx([1.001, 2.002])

if __name__ == "__main__":
    try:
        test_approx()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.