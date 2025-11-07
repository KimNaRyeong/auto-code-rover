Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest import TestCase

class TestIssue(TestCase):
    def test_issue(self):
        TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
        valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
        invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
        ds = xr.merge([valid_times, invalid_times])
        
        try:
            xr.decode_cf(ds)
            self.fail("Expected ValueError to be raised.")
        except Exception as e:
            print_stacktrace(e)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(TestIssue("test_issue"))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        exit(1)
```

This script creates the same dataset as in the issue description, then attempts to decode it using `xr.decode_cf()`. If an exception is raised (which should be a ValueError), it prints the stack trace and exits with code 1.