Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase

class Reproducer(TestCase):
    def test_sum_min_count(self):
        da = xr.DataArray([[1., 2, 3], [4, 5, 6]])
        try:
            da.sum(["dim_0", "dim_1"], min_count=1)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected 'min_count' to be available for reduction with more than one dimension")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Reproducer("test_sum_min_count"))
    result = unittest.TextTestRunner().run(suite)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
```

This script defines a test case `test_sum_min_count` that attempts to call the `sum` method with `min_count=1` on an XArray DataArray. If the operation raises an exception, it prints the stack trace and fails the test.