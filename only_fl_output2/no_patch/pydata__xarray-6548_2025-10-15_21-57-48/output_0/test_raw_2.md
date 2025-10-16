Based on the requirements and the specific function to print a stack trace, the standalone Python file named `reproducer.py`, which is designed to reproduce the reported issue regarding the need for a `name` attribute in the first argument of `xr.polyval`, will be as follows:

```python
# reproducer.py
import xarray as xr

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

def main():
    coeffs = xr.DataArray([1, 2, 3], dims="degree")
    # Creating coord without a name attribute to reproduce the issue
    coord = xr.DataArray([0, 1, 2], dims="x")
    
    try:
        # This operation should raise a KeyError when the issue is present
        result = xr.polyval(coord, coeffs)
    except KeyError as e:
        # Correctly caught the expected KeyError, now printing the stack trace
        print_stacktrace(e)
        assert False, "KeyError raised as expected due to missing name attribute in 'coord'."
    
    # This line should ideally be reached when the issue is fixed and no KeyError is thrown
    print("Issue resolved: `xr.polyval` can now handle coords without a name attribute.")
    exit(0)

if __name__ == "__main__":
    main()
```

This Python script is tailored to verify the specific problem with `xr.polyval` that arises when the first argument lacks a `name` attribute. If the issue persists, a `KeyError` is expected to be thrown; when caught, the script prints a detailed stack trace using the provided function and asserts failure with a message that describes the issue. Conversely, should the operation complete without error, indicating a resolution to the described problem, the script will progress to a success message and exit with code `0`. This setup ensures a clear distinction between reproducing the issue (raising `AssertionError`) and confirming its resolution (normal script completion).