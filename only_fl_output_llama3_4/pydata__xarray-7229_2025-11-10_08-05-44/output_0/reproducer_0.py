import xarray as xr
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

class TestXRWhereKeepAttrs(unittest.TestCase):

    def test_xr_where_keep_attrs(self):
        ds = xr.tutorial.load_dataset("air_temperature")
        with self.assertRaises(AssertionError) as e:
            xr.where(True, ds.air, ds.air, keep_attrs=True).time.attrs
        print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
