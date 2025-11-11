Here is the reproducer script:

```python
import numpy as np

def interpolate(y, x):
    from scipy.interpolate import interp1d
    f = interp1d(np.arange(1, len(y)+2), y, fill_value="extrapolate")
    return f(x)

y = (18, 25, 43, 70, 115)
try:
    result = interpolate(y, 5)
    assert np.isnan(result) == False
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue is fixed")
    exit(0)
```

You can run this script with `python3 reproducer.py` to reproduce the issue.