Here is the reproducer script:

```python
import xarray as xr
import numpy as np
import unittest
from io import StringIO
from contextlib import redirect_stdout

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

        try:
            ds.groupby("id").apply(lambda x: None)
        except Exception as e:
            f = StringIO()
            with redirect_stdout(f):
                print_stacktrace(e)
            self.fail(f.read())

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if the issue is present, it will print the stack trace.