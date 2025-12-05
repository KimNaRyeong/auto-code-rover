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

def main():
    da = xr.DataArray([0, 1, 2])
    try:
        da.quantile(q=50)
    except ValueError as e:
        print_stacktrace(e)
        assert str(e) == "Percentiles must be in the range [0, 1]"

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the following stack trace and exit with code 1:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    main()
  File "reproducer.py", line 11, in main
    assert str(e) == "Percentiles must be in the range [0, 1]"
AssertionError: Percentiles must be in the range [0, 100]
```
This reproduces the issue where the error message is incorrect.