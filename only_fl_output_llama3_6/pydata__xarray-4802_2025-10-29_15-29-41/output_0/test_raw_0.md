Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase

class TestDecodeCF(TestCase):
    def test_decode_cf_fails_with_length_1_list(self):
        ds = xr.DataArray([0, 1, 2], name='foo',
                          attrs={'scale_factor': [0.01],
                                 'add_offset': [1.0]}).to_dataset()
        try:
            xr.decode_cf(ds)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected decode_cf to fail")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestDecodeCF)
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stderr)
    result = runner.run(suite)

    if result.wasSuccessful():
        sys.exit(0)
    else:
        sys.exit(1)
```

This script defines a test case `TestDecodeCF` that creates the dataset with `scale_factor` and `add_offset` as length-1 lists, then attempts to decode it using `xr.decode_cf`. If the decoding fails (i.e., an exception is raised), the script prints the stack trace and fails the test.