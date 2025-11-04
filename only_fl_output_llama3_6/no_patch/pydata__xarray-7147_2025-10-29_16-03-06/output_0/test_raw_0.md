Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest import TestCase

class TestTimeDecodingError(TestCase):

    def test_time_decoding_error(self):
        TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
        valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
        invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
        ds = xr.merge([valid_times, invalid_times])
        
        try:
            xr.decode_cf(ds)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected time decoding error")

if __name__ == "__main__":
    unittest.main()
```

This script creates a minimal example of the issue and attempts to decode it. If an exception is raised, it prints the stack trace using the provided function and fails the test.