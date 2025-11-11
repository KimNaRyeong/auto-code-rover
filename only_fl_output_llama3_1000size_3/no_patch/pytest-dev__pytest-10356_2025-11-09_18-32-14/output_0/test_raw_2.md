Here is the reproducer script:

```python
import pytest
from your_module import Base, Foo, Bar, TestDings  # Replace 'your_module' with the actual module name

def test_reproducer():
    try:
        class TestClass(Foo, Bar):
            pass
        assert len(pytest.mark) == 2
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Expected pytest to not lose markers")

if __name__ == "__main__":
    test_reproducer()
```

This script will create a new class that inherits from `Foo` and `Bar`, and then assert that the number of markers is 2. If the issue is present, it should print the stack trace and raise an `AssertionError`.