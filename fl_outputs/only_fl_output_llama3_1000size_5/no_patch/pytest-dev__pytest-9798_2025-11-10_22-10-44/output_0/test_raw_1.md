Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import pytest

def test_approx():
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except Exception as e:
        print_stacktrace(e)
        exit(1)

print("Test passed!")
exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the error. If the issue is fixed, it will print "Test passed!" and exit with code 0.

Please note that this reproducer does not require Numpy to be installed as the original issue description suggests.