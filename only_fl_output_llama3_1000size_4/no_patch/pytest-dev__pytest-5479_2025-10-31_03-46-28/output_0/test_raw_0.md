Here is the reproducer script:

```python
import pytest
from unittest import assert_

def test_u():
    with pytest.raises(AssertionError, match=u"\u2603"):
        assert False, u"\u2603"

try:
    test_u()
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```

This script should reproduce the issue when run with Python 2. It will raise an `AssertionError` and print a stack trace to the console.