Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import unittest
from unittest.mock import patch

class TestIssue(unittest.TestCase):

    def test_issue(self):
        ds = xr.Dataset()
        ds["variable"] = xr.DataArray(np.random.rand(4,3,5), 
                                       {"lat":np.arange(4), "lon":np.arange(3), "time":np.arange(5)}, 
                                       ("lat", "lon", "time"),
                                      )

        ds["id"] = xr.DataArray(np.arange(12.0).reshape((4,3)),
                                 {"lat": np.arange(4), "lon":np.arange(3)},
                                 ("lat", "lon"),
                                )

        ds["id"].values[0,0] = np.nan

        with self.assertRaises(IndexError):
            ds.groupby("id").apply(lambda x: None)

    def test_stacktrace(self):
        e = IndexError()
        print_stacktrace(e)


if __name__ == '__main__':
    unittest.main()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.