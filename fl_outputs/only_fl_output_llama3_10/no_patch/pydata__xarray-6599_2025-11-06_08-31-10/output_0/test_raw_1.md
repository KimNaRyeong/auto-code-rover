Here is the reproducer script:

```Python
import xarray as xr
import numpy as np

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

    result = xr.polyval(azimuth_time, polyfit_coefficients)

    if not np.allclose(result.values, [[4447392.16, 1450539.74, 5299608.57],
                                        [4505537.25588366, 1448882.82238152, 5250846.359196],
                                        [4563174.92026797, 1446979.12250014, 5201491.44401733],
                                        [4620298.31815291, 1444829.59596699, 5151549.377964],
                                        [4676900.67053846, 1442435.23739315, 5101025.78153601],
                                        [4732975.25442459, 1439797.08038974, 5049926.34223336]]):
        raise AssertionError("Expected result is not correct")

except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

You can run this script with `python3 reproducer.py` to reproduce the issue.