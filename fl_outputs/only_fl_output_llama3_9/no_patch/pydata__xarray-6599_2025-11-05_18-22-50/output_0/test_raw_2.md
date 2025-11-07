The issue seems to be related to the removal of `np.unicode_` in NumPy 2.0, which is not compatible with your environment.

Here's an updated reproducer script that should work:

```python
import xarray as xr
import numpy as np

def main():
    values = np.array([
        "2021-04-01T05:25:19.000000000",
        "2021-04-01T05:25:29.000000000",
        "2021-04-01T05:25:39.000000000",
        "2021-04-01T05:25:49.000000000",
        "2021-04-01T05:25:59.000000000",
        "2021-04-01T05:26:09.000000000",
    ], dtype="datetime64[ns]")
    azimuth_time = xr.DataArray(values, name="azimuth_time", coords={"azimuth_time": values - values[0]})

    polyfit_coefficients = xr.DataArray([
        [2.33333335e-43, 1.62499999e-43, 2.79166678e-43],
        [-1.15316667e-30, 1.49518518e-31, 9.08833333e-31],
        [-2.50272583e-18, -1.23851062e-18, -2.99098229e-18],
        [5.83965193e-06, -1.53321770e-07, -4.84640242e-06],
        [4.44739216e06, 1.45053974e06, 5.29960857e06],
    ], dims=("degree", "axis"), coords={"axis": [0, 1, 2], "degree": [4, 3, 2, 1, 0]})

    try:
        result = xr.polyval(azimuth_time, polyfit_coefficients)
        assert result.shape == (6, 3), f"Expected shape {(6, 3)}, got {result.shape}"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```

This script should raise an `AssertionError` when the issue is present and print a stack trace using the provided function.