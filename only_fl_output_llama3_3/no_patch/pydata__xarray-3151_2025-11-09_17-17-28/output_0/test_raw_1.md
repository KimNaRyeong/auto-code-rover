Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import unittest
from unittest.mock import patch
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

class TestReproducer(unittest.TestCase):

    @patch('sys.stdout.write')
    def test_reproduce_issue(self, mock_stdout):
        try:
            import xarray as xr
            import numpy as np

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

            with self.assertRaises(ValueError):
                ds3 = xr.combine_by_coords((ds1, ds2))

        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    unittest.main()
```

This script will run the reproduce code and if it raises an error, it will print the stack trace.