Here is the reproducer script:

```python
import numpy as np
import xarray as xr
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestCombineByCoords(unittest.TestCase):

    def test_combine_by_coords(self):
        try:
            x1 = xr.Dataset(
                {
                    "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
                },
                coords={"y": [0, 1], "x": [10, 20, 30]},
            )
            x2 = xr.Dataset(
                {
                    "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
                },
                coords={"y": [2, 3], "x": [10, 20, 30]},
            )
            x3 = xr.Dataset(
                {
                    "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
                },
                coords={"y": [2, 3], "x": [40, 50, 60]},
            )
            with redirect_stdout(StringIO()):
                xr.combine_by_coords([x1,x2,x3])
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected no exception")

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if any exception is raised during the execution of `xr.combine_by_coords([x1,x2,x3])`, it will catch that exception, print the stack trace using the provided function, and then fail the test.