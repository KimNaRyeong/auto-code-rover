Here is the reproducer script:

```python
import numpy as np
import xarray as xr
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        n = 5

        d1 = np.arange(n)
        np.random.shuffle(d1)
        A = xr.DataArray(np.ones(n), coords=[('dim', d1)])

        d2 = np.arange(n)
        np.random.shuffle(d2)
        B = xr.DataArray(np.ones(n), coords=[('dim', d2)])

        try:
            print(A + B)  # This works fine
            A += B  # This should also work fine, but it fails
        except Exception as e:
            print_stacktrace(e)
            self.fail("In-place addition failed")

if __name__ == "__main__":
    Reproducer().test_issue()
```

This script creates two DataArrays with the same dimension but in a different order. It then attempts to add them using both `A + B` and `A += B`. If the in-place addition fails, it prints the stack trace and exits with code 1.