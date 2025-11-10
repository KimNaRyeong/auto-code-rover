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
    else:
        print("Test passed.")
        exit(0)

if __name__ == "__main__":
    test_approx()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will print "Test passed." and exit with code 0.

Please note that this reproducer script should be run in the same environment where you encountered the original issue (i.e., with pytest installed).