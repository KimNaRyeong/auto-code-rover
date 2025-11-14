Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import pytest

def test_approx():
    try:
        assert [1, 2] == pytest.approx([1.001, 2.002])
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

    print("Test passed successfully.")
    exit(0)

if __name__ == "__main__":
    test_approx()
```

This script will run the `test_approx` function and catch any `AssertionError` exceptions. If an exception is caught, it will print the stack trace using the provided `print_stacktrace` function and exit with code 1. If no exception is caught, it will print a success message and exit with code 0.

Please note that this script should be executed in a Python environment where pytest is installed.