Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase

class Reproducer(TestCase):

    def test_drop_sel(self):
        data = np.random.randn(2, 3)
        ds = xr.Dataset({"A": (["x", "y"], data)})
        
        try:
            ds.drop_sel(y=[1])
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected drop_sel to work without coordinates")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    if not result.wasSuccessful():
        exit(1)
```

This script defines a test case that attempts to drop the index `y=1` from the dataset. If an exception is raised, it prints the stack trace and fails the test.