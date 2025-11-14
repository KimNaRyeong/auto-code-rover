Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        data = np.random.randn(2, 3)
        ds = xr.Dataset({"A": (["x", "y"], data)})
        
        try:
            ds.drop_sel(y=[1])
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected drop_sel to work without coordinates")

if __name__ == "__main__":
    test_result = Reproducer().run()
    if not test_result:
        exit(0)
    else:
        raise AssertionError("Issue still present")
```

This script creates a simple xarray dataset, tries to drop the index `y` with value 1 using `drop_sel`, and checks if an exception is raised. If an exception is raised, it prints the stack trace and fails the test.