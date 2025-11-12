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

    assert set(a) == set(b), "Sets are equal but pytest.approx() fails"
    assert set(a) != pytest.approx(set(b)), "pytest.approx() should not work with sets"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```

This script will run the test and if it fails, it will print the stack trace of the `AssertionError` and exit with code 1.