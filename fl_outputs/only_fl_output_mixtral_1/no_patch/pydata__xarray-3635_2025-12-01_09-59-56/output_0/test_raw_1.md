 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    da = xr.DataArray([0, 1, 2])
    try:
        da.quantile(q=50)
    except ValueError as e:
        print_stacktrace(e)
        assert e.args[0] == "Percentiles must be in the range [0, 1]"
    else:
        print("Test passed without expected ValueError")
        assert False
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    assert e.args[0] == "Percentiles must be in the range [0, 1]"
AssertionError: Percentiles must be in the range [0, 100]
```
This indicates that the issue is present, as the error message is still `Percentiles must be in the range [0, 100]` instead of the expected `Percentiles must be in the range [0, 1]`.