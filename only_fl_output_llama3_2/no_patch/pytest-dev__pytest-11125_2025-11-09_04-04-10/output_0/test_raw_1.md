Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import pytest
from _pytest.config.argparsing import ParserError

def pytest_addoption(parser):
    parser.addoption("--run-podman", action="store_true", default=False, help="run podman tests")

def main():
    try:
        pytest.main(["unit_test", "--run-podman"])
    except ParserError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    main()
```

This script defines a `pytest_addoption` function that adds the same option as in your original code. Then, it calls `pytest.main` with the same arguments and catches any `ParserError` exceptions raised by Pytest. If an exception is caught, it prints the stack trace using the provided `print_stacktrace` function and raises an `AssertionError`.