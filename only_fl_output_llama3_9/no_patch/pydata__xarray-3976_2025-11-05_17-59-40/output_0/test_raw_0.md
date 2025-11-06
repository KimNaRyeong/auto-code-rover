Here is the reproducer script:

```python
import numpy as np
import xarray as xr
from unittest import TestCase

class Reproducer(TestCase):
    def test_reproducer(self):
        n = 5

        d1 = np.arange(n)
        np.random.shuffle(d1)
        A = xr.DataArray(np.ones(n), coords=[('dim', d1)])

        d2 = np.arange(n)
        np.random.shuffle(d2)
        B = xr.DataArray(np.ones(n), coords=[('dim', d2)])

        try:
            print(A + B)
            A += B
        except Exception as e:
            print_stacktrace(e)
            self.fail()

if __name__ == "__main__":
    Reproducer().test_reproducer()
```

This script is a test case that reproduces the issue. It creates two DataArrays `A` and `B` with the same dimension but in different order, then tries to add them using both `A + B` and `A += B`. If any exception occurs during this process, it prints the stack trace and fails the test.