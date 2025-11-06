Here is the reproducer script:

```Python
import xarray as xr
import numpy as np
import unittest
from unittest.mock import patch

class TestIssue(unittest.IsolatedTestCase):
    def test_issue(self):
        ds = xr.Dataset(coords={'a': np.array([0], dtype='i4')})
        with self.assertRaises(AssertionError):
            self.assertFalse(ds['a'].values.dtype == ds.stack(b=('a',))['a'].values.dtype)

if __name__ == '__main__':
    unittest.main()
```

This script will run the test and if the issue is present, it will raise an `AssertionError` and print a stack trace.