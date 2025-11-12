Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        yCoord = ['a', 'c', 'b']  # raises ValueError on combine
        ds1 = xr.Dataset(
            data_vars=dict(
                data=(['x', 'y'], np.random.rand(3, 3))
            ),
            coords=dict(
                x=[1, 2, 3],
                y=yCoord
            )
        )

        ds2 = xr.Dataset(
            data_vars=dict(
                data=(['x', 'y'], np.random.rand(4, 3))
            ),
            coords=dict(
                x=[4, 5, 6, 7],
                y=yCoord
            )
        )

        try:
            ds3 = xr.combine_by_coords((ds1, ds2))
        except ValueError as e:
            print_stacktrace(e)
            self.fail("Expected combine_by_coords to work with non-monotonic coordinates")

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Reproducer("test_issue"))
    runner = unittest.TextTestRunner(failfast=True)
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
```

This script defines a test case `test_issue` that attempts to combine two datasets with non-monotonic coordinates. If the combination raises a `ValueError`, it prints the stack trace and fails the test.