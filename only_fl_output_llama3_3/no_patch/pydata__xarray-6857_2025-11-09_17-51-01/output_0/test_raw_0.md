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
                result = str(da_withunits == da_withoutunits)
                f = StringIO()
                with patch('sys.stdout', f) as mock_stdout:
                    print(result)
                    print_stacktrace(e)

        self.fail("Expected AssertionError")

if __name__ == '__main__':
    unittest.main()
```

This script will run the test and if the issue is present, it will raise an `AssertionError` and print a stack trace.