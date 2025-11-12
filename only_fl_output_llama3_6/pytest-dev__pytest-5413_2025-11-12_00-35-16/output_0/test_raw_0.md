Here is the reproducer script:

```Python
import pytest
from your_module import YourException  # replace with actual module and exception name

def test_reproducer():
    try:
        raise YourException(
            f"A\n"
            f"B\n"
            f"C"
        )
    except YourException as e:
        print(str(e))

    with pytest.raises(YourException) as e:
        raise YourException(
            f"A\n"
            f"B\n"
            f"C"
        )

    assert str(e) == "A\nB\nC", "Expected the full error message, but got {}".format(str(e.value))
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.