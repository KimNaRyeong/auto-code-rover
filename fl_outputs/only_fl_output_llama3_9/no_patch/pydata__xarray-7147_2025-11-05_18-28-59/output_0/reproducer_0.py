import xarray as xr
import unittest
from unittest.mock import patch
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestIssue(unittest.IsolatedAsyncioTestCase):
    @patch('sys.stdout', new_callable=StringIO)
    async def test_issue(self, mock_stdout):
        TIME_ATTRS = {"units": "days since 0001-01-01", "calendar": "noleap"}
        valid_times = xr.DataArray([0, 1], dims=["time"], attrs=TIME_ATTRS, name="valid_times")
        invalid_times = xr.DataArray([1e36, 2e36], dims=["time"], attrs=TIME_ATTRS, name="invalid_times")
        ds = xr.merge([valid_times, invalid_times])
        
        try:
            xr.decode_cf(ds)
        except Exception as e:
            print_stacktrace(e)
            self.fail("Expected error message to include problematic variable's name")

if __name__ == "__main__":
    unittest.main()
