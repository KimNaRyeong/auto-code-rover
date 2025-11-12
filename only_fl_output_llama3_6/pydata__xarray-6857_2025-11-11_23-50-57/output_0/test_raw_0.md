Here is the reproducer script:

```Python
import xarray as xr
import unittest
from unittest.mock import patch
from io import StringIO
from contextlib import redirect_stdout

class TestIssue(unittest.TestCase):

    def test_issue(self):
        with self.assertRaises(AssertionError) as e:
            with redirect_stdout(StringIO()):
                da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
                da_withunits.frequency.attrs["units"] = "GHz"
                print(da_withunits.frequency.units)
                da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
                print(da_withunits == da_withoutunits)
                print(da_withunits.frequency.units)

        f = StringIO()
        with patch('sys.stdout', f) as mock_stdout:
            print_stacktrace(e)

    def test_issue_fixed(self):
        try:
            da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
            da_withunits.frequency.attrs["units"] = "GHz"
            print(da_withunits.frequency.units)
            da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
            print(da_withunits == da_withoutunits)
            print(da_withunits.frequency.units)
        except Exception as e:
            f = StringIO()
            with patch('sys.stdout', f) as mock_stdout:
                print_stacktrace(e)
            self.fail()

if __name__ == '__main__':
    unittest.main()
```

This script will run two tests: `test_issue` and `test_issue_fixed`. The first test is expected to raise an `AssertionError`, which means the issue should be present. The second test is expected not to raise any exceptions, which means the issue should be fixed.