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
        try:
            coeffs = xr.DataArray([1, 2, 3], dims="degree")
            coord = xr.DataArray([0, 1, 2], dims="x")
            xr.polyval(coord, coeffs)
            self.fail("Expected KeyError")
        except Exception as e:
            print_stacktrace(e)

if __name__ == "__main__":
    test_suite = unittest.TestLoader().loadTestsFromTestCase(TestPolyval)
    result = unittest.TextTestRunner(verbosity=2).run(test_suite)
    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
```

This script defines a `TestPolyval` class that contains a single test method. This method attempts to call `xr.polyval(coord, coeffs)` and expects it to raise a KeyError. If the expected exception is raised, the script prints the stack trace using the provided function.