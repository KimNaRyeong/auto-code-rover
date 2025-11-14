Here is the reproducer script:

```python
import xarray as xr
import numpy as np
from unittest import TestCase
import sys
import traceback

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

    def test_reproducer(self):
        yCoord = ['a', 'c', 'b']  # raises ValueError on combine
        ds1 = xr.Dataset(
            data_vars=dict(
                data=(['x', 'y'], np.random.rand(3, 3))
            ),
            coords=dict(
                x=[1, 2, 3],
                y=yCoord
            )
        )

        ds2 = xr.Dataset(
            data_vars=dict(
                data=(['x', 'y'], np.random.rand(4, 3))
            ),
            coords=dict(
                x=[4, 5, 6, 7],
                y=yCoord
            )
        )

        try:
            xr.combine_by_coords((ds1, ds2))
        except ValueError as e:
            print_stacktrace(e)
            self.fail("Expected combine_by_coords to work with non-monotonic coordinates")

if __name__ == "__main__":
    test_suite = unittest.TestSuite()
    test_suite.addTest(Reproducer('test_reproducer'))
    runner = unittest.TextTestRunner()
    result = runner.run(test_suite)

    if not result.wasSuccessful():
        sys.exit(1)
```

This script defines a `Reproducer` class that inherits from `unittest.TestCase`. The `test_reproducer` method attempts to combine the two datasets using `xr.combine_by_coords`. If an error occurs, it prints the stack trace and fails the test.