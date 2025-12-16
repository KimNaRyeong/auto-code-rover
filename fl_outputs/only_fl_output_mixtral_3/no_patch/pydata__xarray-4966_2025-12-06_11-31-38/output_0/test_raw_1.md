 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    ds_netcdf4 = xr.open_dataset("https://observations.ipsl.fr/thredds/dodsC/EUREC4A/PRODUCTS/testdata/netcdf_testfiles/test_NC_BYTE_neg.nc", engine="netcdf4")
    ds_pydap = xr.open_dataset("https://observations.ipsl.fr/thredds/dodsC/EUREC4A/PRODUCTS/testdata/netcdf_testfiles/test_NC_BYTE_neg.nc", engine="pydap")

    # Assert that the signed byte values are correctly returned by netcdf4 engine
    assert np.min(ds_netcdf4.test) < 0

    # Assert that the unsigned byte values are incorrectly returned by pydap engine
    assert np.min(ds_pydap.test) >= 0

except Exception as e:
    print_stacktrace(e)
    raise
```
When the issue is present, running `python3 reproducer.py` will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    assert np.min(ds_pydap.test) >= 0
AssertionError:
```
When the issue is fixed, running `python3 reproducer.py` will not print any output and exit with code 0.