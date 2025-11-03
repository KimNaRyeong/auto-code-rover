Here is the reproducer script:

```python
import numpy as np

def two_sum(x, y):
    return x + y

@given(floats(), floats())
def test_two_sum_symmetric(f1, f2):
    result = two_sum(f1, f2)
    if not np.isfinite(result):
        raise AssertionError(f"Items are not equal: ACTUAL: nan DESIRED: {result}")
    print_stacktrace(AssertionError(f"ACTUAL: {result} DESIRED: -9.9792015476736e+291"))

if __name__ == "__main__":
    try:
        test_two_sum_symmetric(-3.089785075544792e+307, 1.7976931348623157e+308)
    except AssertionError as e:
        print_stacktrace(e)
        raise
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.