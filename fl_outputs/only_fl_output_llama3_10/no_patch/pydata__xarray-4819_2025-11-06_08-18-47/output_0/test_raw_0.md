Here is the reproducer script:

```python
import numpy as np
import xarray as xr
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
    def test_issue(self):
        data = np.random.randn(2, 3)
        ds = xr.Dataset({"A": (["x", "y"], data)})
        try:
            ds.drop_sel(y=[1])
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected drop_sel to work without coordinates")

if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(Reproducer)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
```

This script creates a test case that attempts to drop an index from the "y" dimension of the dataset. If the `drop_sel` method raises an exception, it prints the stack trace and fails the test.