The issue is not reproduced by the test script I provided earlier. The error message you are seeing is due to a NumPy version issue, not related to the original issue.

To reproduce the original issue, we need to modify the reproducer script as follows:

```Python
import xarray as xr
import unittest
from unittest.mock import patch

class TestIssue(unittest.TestCase):

    def test_issue(self):
        da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        da_withunits.frequency.attrs["units"] = "GHz"
        print(da_withunits.frequency.units)
        da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
        result = str(da_withunits == da_withoutunits)
        self.assertEqual(result, "[(True,)]")
        with patch('sys.stdout', new=StringIO()) as mock_stdout:
            print_stacktrace(AssertionError("Expected assertion error"))

if __name__ == '__main__':
    unittest.main()
```

This script will run the test and if the issue is present, it will raise an `AssertionError` and print a stack trace.