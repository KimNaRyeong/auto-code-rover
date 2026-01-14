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

try:
    import xarray as xr
    import numpy as np

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

    expected = np.array([
        [4447392.16, 1450539.74, 5299608.57],
        [4505537.26, 1448882.82, 5250846.36],
        [4563174.92, 1446979.12, 5201491.44],
        [4620298.32, 1444829.60, 5151549.38],
        [4676900.67, 1442435.24, 5101025.78],
        [4732975.25, 1439797.08, 5049926.34]
    ])

    results = xr.polyval(azimuth_time, polyfit_coefficients)
    np.testing.assert_allclose(results.values, expected, rtol=1e-5)

except AssertionError as e:
    print_stacktrace(e)
    raise
except Exception as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue not present, exiting with code 0.")
    exit(0)
```