Here is the reproducer script:

```Python
import xarray as xr
from unittest import TestCase

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestPolyval(TestCase):
    def test_polyval(self):
        coeffs = xr.DataArray([1, 2, 3], dims="degree")

        # With a "handmade" coordinate it fails:
        coord = xr.DataArray([0, 1, 2], dims="x")

        try:
            xr.polyval(coord, coeffs)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected xr.polyval to work with handmade coordinates")

    def test_polyval_with_named_coord(self):
        coeffs = xr.DataArray([1, 2, 3], dims="degree")

        # With a "handmade" coordinate and name it works:
        coord = xr.DataArray([0, 1, 2], dims="x", name="x")
        try:
            xr.polyval(coord, coeffs)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected xr.polyval to work with handmade coordinates and names")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(TestPolyval)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)

    if not result.wasSuccessful():
        sys.exit(1)
```

This script will run two tests: one for the original issue and another for the fix. If any of these tests fail, it will print the stack trace and exit with code 1.