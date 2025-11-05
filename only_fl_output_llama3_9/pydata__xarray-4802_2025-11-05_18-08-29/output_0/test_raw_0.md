Here is the reproducer script:

```python
import xarray as xr
import numpy as np
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

class Reproducer(TestCase):
    def test_decode_cf_fails_with_length_1_list(self):
        ds = xr.DataArray([0, 1, 2], name='foo',
                          attrs={'scale_factor': [0.01],
                                 'add_offset': [1.0]}).to_dataset()
        try:
            xr.decode_cf(ds)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected decode_cf to fail")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    test_result = unittest.TextTestRunner(verbosity=2).run(suite)

    if any((res.result.__class__.__name__ in ["Failure", "Error"] for res in test_result.results)):
        sys.exit(1)
    else:
        sys.exit(0)
```

This script defines a `Reproducer` class that contains a single test method. This method creates an xarray dataset with a length-1 list as the value of the 'scale_factor' attribute, then attempts to decode the CF conventions using `xr.decode_cf`. If the decoding fails (i.e., an exception is raised), it prints the stack trace and fails the test.