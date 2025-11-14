Here is the reproducer script:

```Python
import pytest
from your_module import YourClass  # replace with actual module and class name

def test_issue():
    try:
        raise LookupError(
            f"A\n"
            f"B\n"
            f"C"
        )
    except LookupError as e:
        print(str(e))

    with pytest.raises(LookupError) as e:
        raise LookupError(
            f"A\n"
            f"B\n"
            f"C"
        )

    try:
        str(e)
    except AssertionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    test_issue()
```

This script will reproduce the issue and print a stack trace if it is present.