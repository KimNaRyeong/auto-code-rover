Here is the reproducer script:

```python
import pytest
from _pytest.config.argparsing import ParserError

def test_reproducer():
    try:
        pytest.main(['-k', 'test_solution[foo.py-5\\n10\\n-16\\n]'])
    except ParserError as e:
        print_stacktrace(e)
        assert False, "Expected ParserError"

if __name__ == "__main__":
    test_reproducer()
```

This script will raise a `ParserError` when the issue is present and print the stack trace.