Here is the reproducer script:

```python
import xarray as xr
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestQuantileKeepAttrs(unittest.TestCase):

    def test_quantile_keep_attrs(self):
        try:
            da = xr.DataArray([0, 0], dims="x", attrs={'units':'K'})
            out = da.quantile(.9, dim='x', keep_attrs=True)
            with redirect_stdout(StringIO()):
                print(out.attrs)
            self.assertEqual({'units': 'K'}, out.attrs)
        except AssertionError as e:
            f = StringIO()
            with redirect_stdout(f):
                print_stacktrace(e)
            print(f.read(), file=sys.stderr)
            self.fail()

if __name__ == '__main__':
    unittest.main()
```

This script defines a test case that attempts to reproduce the issue. It creates an `xarray.DataArray` and then calls its `quantile` method with `keep_attrs=True`. The script then checks if the resulting data array's attributes are as expected. If they are not, it prints the stack trace of the exception and fails the test.