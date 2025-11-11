Here is the reproducer script:

```python
import numpy as np
import xarray as xr
import unittest

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

class TestCombineByCoords(unittest.TestCase):

    def test_combine_by_coords(self):
        x1 = xr.Dataset(
            {
                "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
            },
            coords={"y": [0, 1], "x": [10, 20, 30]},
        )
        x2 = xr.Dataset(
            {
                "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
            },
            coords={"y": [2, 3], "x": [10, 20, 30]},
        )
        x3 = xr.Dataset(
            {
                "temperature": (("y", "x"), 20 * np.random.rand(6).reshape(2, 3))
            },
            coords={"y": [2, 3], "x": [40, 50, 60]},
        )

        try:
            xr.combine_by_coords([x1,x2,x3])
        except ValueError as e:
            print_stacktrace(e)
            self.fail("Expected combine_by_coords to not raise an error")

if __name__ == "__main__":
    unittest.main()
```

This script defines a test case that attempts to call `xr.combine_by_coords` with the given datasets. If an error is raised, it prints the stack trace and fails the test.

To reproduce the issue, simply run this script using Python: `python3 reproducer.py`.