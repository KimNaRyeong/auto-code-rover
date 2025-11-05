Here is the reproducer script:

```Python
import xarray as xr
from unittest import TestCase

class Reproducer(TestCase):
    def test_polyval(self):
        coeffs = xr.DataArray([1, 2, 3], dims="degree")

        # With a "handmade" coordinate it fails:
        coord = xr.DataArray([0, 1, 2], dims="x")

        try:
            xr.polyval(coord, coeffs)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected xr.polyval to raise KeyError")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
```

This script will run the test case and print a stack trace if the issue is present. If the issue is fixed, it will exit with code 0.