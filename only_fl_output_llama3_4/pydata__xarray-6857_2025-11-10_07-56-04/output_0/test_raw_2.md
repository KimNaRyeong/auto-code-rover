Here is the reproducer script:

```Python
import xarray as xr
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestIssue(unittest.TestCase):

    def test_issue(self):
        da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        da_withunits.frequency.attrs["units"] = "GHz"
        print(da_withunits.frequency.units)
        da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        try:
            result = da_withunits == da_withoutunits
            self.assertTrue(result.all())
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected no exception")

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if an assertion error is raised, it will print the stack trace.