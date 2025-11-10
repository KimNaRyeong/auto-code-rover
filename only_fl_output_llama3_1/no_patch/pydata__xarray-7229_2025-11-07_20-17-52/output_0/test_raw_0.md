Here is the reproducer script:

```python
import xarray as xr
import unittest
from unittest.mock import patch

class TestXRWhereKeepAttrs(unittest.TestCase):

    @patch('xarray.core.common._get_coord_attrs')
    def test.xr_where_keep_attrs(self, mock_get_coord_attrs):
        ds = xr.tutorial.load_dataset("air_temperature")
        result = xr.where(True, ds.air, ds.air, keep_attrs=True)
        self.assertEqual(result.time.attrs, {'standard_name': 'time', 'long_name': 'Time'})

if __name__ == '__main__':
    unittest.main()
```

You can run this script using `python3 reproducer.py` and it should raise an `AssertionError` when the issue is present.