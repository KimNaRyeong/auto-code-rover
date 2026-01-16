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

def main():
    import xarray as xr
    import pandas as pd
    time_coord = pd.date_range("2020-01-01","2020-01-03", freq="12H")
    da = xr.DataArray([1,2,3,4,5], dims=["time"], coords={'time': time_coord})

    print("Trying to access `time` attribute:")
    print(da.time.dt.time)
    try:
        print("\nTrying to access `date` attribute:")
        print(da.time.dt.date)  # This should raise AttributeError
        # If no exception is raised, we assert failure as the issue is expected to be present.
        assert False, "Expected an AttributeError for missing 'date' attribute"
    except AttributeError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```