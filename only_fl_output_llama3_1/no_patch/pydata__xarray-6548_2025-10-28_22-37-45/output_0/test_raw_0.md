Here is the reproducer script:

```Python
import xarray as xr
from unittest import TestCase

class Reproducer(TestCase):
    def test_reproducer(self):
        try:
            coeffs = xr.DataArray([1, 2, 3], dims="degree")
            coord = xr.DataArray([0, 1, 2], dims="x")
            xr.polyval(coord, coeffs)
            self.fail("Expected KeyError")
        except Exception as e:
            print_stacktrace(e)

if __name__ == "__main__":
    Reproducer().run()
```

This script will run the test and if the issue is present, it will raise an `AssertionError` with a stack trace.