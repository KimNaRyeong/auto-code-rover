Here is the reproducer script:

```python
from scipy.interpolate import interp1d

def interpolate(y, x):
    f = interp1d(range(1, len(y)+1), y, fill_value="extrapolate")
    return f(x)

y = (18, 25, 43, 70, 115)
try:
    result = interpolate(y, 5)
    assert not np.isnan(result)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed")
    exit(0)
```

This script should reproduce the issue and raise an `AssertionError` when the interpolation at 5 returns `nan`.