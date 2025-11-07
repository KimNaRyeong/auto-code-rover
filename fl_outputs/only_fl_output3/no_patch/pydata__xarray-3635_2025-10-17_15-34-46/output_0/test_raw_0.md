```python
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

def run_test():
    # Importing xarray library
    import xarray as xr
    
    # Creating a DataArray
    da = xr.DataArray([0, 1, 2])
    
    try:
        # Attempting to compute quantiles
        result = da.quantile(q=50)
        # Expected an error; if not raised, the test fails.
        raise AssertionError("Expected a ValueError for quantile range but none occurred.")
    except ValueError as e:
        # Check if the error message is what we expect
        correct_message = "Quantiles must be in the range [0, 1]"
        if str(e) != correct_message:
            # If the message is wrong, print the stack trace and re-raise the exception
            print_stacktrace(e)
        else:
            # Error message as expected; issue is resolved.
            print("Test passed: ValueError raised with expected message.")

if __name__ == "__main__":
    try:
        run_test()
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as ex:
        print_stacktrace(ex)
```