Here is the reproducer script:

```python
import xarray as xr
from unittest import TestCase
import traceback
import sys

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
        try:
            import xarray as xr
            da = xr.DataArray([0, 0], dims="x", attrs={'units':'K'})
            out = da.quantile(.9, dim='x', keep_attrs=True)
            if not out.attrs:
                raise AssertionError("DataArray.quantile does not honor `keep_attrs`")
        except Exception as e:
            print_stacktrace(e)
            self.fail()

if __name__ == '__main__':
    Reproducer().test_reproducer()
```

This script will run the test and if the issue is present, it will raise an AssertionError and print a stack trace.