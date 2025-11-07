Certainly! Based on your requirements, below is a Python script designed to reproduce the reported issue with `polyval` and `timedelta64` coordinates. If the issue is present, the script will raise an `AssertionError` and print a stack trace showing where the error occurred. If the issue is not present, the script will simply print "No issue detected" and exit with code 0, indicating success.

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
    import numpy as np

    values = np.array(
        [
            "2021-04-01T05:25:19.000000000",
            "2021-04-01T05:25:29.000000000",
            "2021-04-01T05:25:39.000000000",
            "2021-04-01T05:25:49.000000000",
            "2021-04-01T05:25:59.000000000",
            "2021-04-01T05:26:09.000000000",
        ],
        dtype="datetime64[ns]",
    )
    azimuth_time = xr.DataArray(
        values, name="azimuth_time", coords={"azimuth_time": values - values[0]}
    )

    polyfit_coefficients = xr.DataArray(
        [
            [2.33333335e-43, 1.62499999e-43, 2.79166678e-43],
            [-1.15316667e-30, 1.49518518e-31, 9.08833333e-31],
            [-2.50272583e-18, -1.23851062e-18, -2.99098229e-18],
            [5.83965193e-06, -1.53321770e-07, -4.84640242e-06],
            [4.44739216e06, 1.45053974e06, 5.29960857e06],
        ],
        dims=("degree", "axis"),
        coords={"axis": [0, 1, 2], "degree": [4, 3, 2, 1, 0]},
    )

    try:
        result = xr.polyval(azimuth_time, polyfit_coefficients)
        expected_shape = (6, 3)  # Assuming the expected result shape should be the same as in the correct results
        assert result.shape == expected_shape, f"Incorrect result shape. Expected: {expected_shape}, Got: {result.shape}"
        print("No issue detected.")
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with error code 1 when the issue is present

if __name__ == "__main__":
    main()
```

This script follows the steps described in your issue reproduction requirements: 
- It sets up a sample dataset using `xarray` and `numpy`.
- Calculates the result of `xr.polyval` with the given `azimuth_time` and `polyfit_coefficients`.
- Asserts that the shape of the resulting dataset matches the expected shape (as detailed in your instructions, assuming the presence of the issue would alter this shape or the execution itself).
- If an error is caught or the assertion fails, it prints the stack trace and exits with a non-zero code to indicate failure.
- Completes successfully with a message and exit code 0 if no issue is found (i.e., if the results match expectations and no errors are raised).

Ensure `xarray`, `numpy`, and all their dependencies are installed in your environment before running this script.