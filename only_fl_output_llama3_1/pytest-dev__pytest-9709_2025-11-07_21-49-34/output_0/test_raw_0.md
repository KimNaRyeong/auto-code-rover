Here is the reproducer script:

```python
import pytest
import numpy as np

def main():
    a = 2**np.arange(12)
    b = 2**np.arange(12)
    np.random.shuffle(a)

    print(*set(a))
    print(*set(b))

    assert set(a) == pytest.approx(set(b))

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script will reproduce the issue by comparing two sets using `pytest.approx()` and asserting that they are equal. If the assertion fails, it will print a stack trace and exit with code 1.