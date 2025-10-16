# reproducer.py
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        import xarray as xr
        import numpy as np

        def standardize(x):
            return (x - x.mean()) / x.std()

        ds = xr.Dataset()
        ds["variable"] = xr.DataArray(np.random.rand(4, 3, 5),
                                      {"lat": np.arange(4), "lon": np.arange(3), "time": np.arange(5)},
                                      ("lat", "lon", "time"))

        ds["id"] = xr.DataArray(np.arange(12.0).reshape((4, 3)),
                                {"lat": np.arange(4), "lon": np.arange(3)},
                                ("lat", "lon"))

        # Introducing a NaN to potentially cause the issue
        ds["id"].values[0, 0] = np.nan

        # This operation is expected to possibly raise an error
        ds.groupby("id").apply(standardize)
        
        # If the operation succeeds without raising an Exception, then the issue is not present
        print("Issue not present, exited with code 0.")
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        # AssertionError is raised to indicate the presence of the issue described
        raise AssertionError("The issue is present.")

if __name__ == "__main__":
    main()
