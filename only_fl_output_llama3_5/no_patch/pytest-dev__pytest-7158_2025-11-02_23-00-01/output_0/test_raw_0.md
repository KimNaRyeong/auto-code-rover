Here is the reproducer script:

```python
import pytest
import os
from _pytest.config.argparsing import ParserError

def test_reproducer():
    try:
        pytest.main(['-rs', '../my_tests/test1.py'])
    except ParserError as e:
        print_stacktrace(e)
        raise AssertionError("Issue present")

if __name__ == "__main__":
    test_reproducer()
```

This script calls `pytest` with the same command as in your example, and catches any `ParserError` that might be raised. If an error is caught, it prints a stack trace using the provided function and raises an `AssertionError`.