Here is the reproducer script:

```python
import numpy as np

def interpolate(y, x):
    from scipy.interpolate import interp1d
    f = interp1d(np.arange(1, len(y)+2), y, bounds_error=False)
    return f(x)

y = (18, 25, 43, 70, 115)
try:
    result = interpolate(y, 5)
    assert np.isnan(result) == False, "Expected value instead of nan"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
else:
    print("Issue fixed")
    exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace. If the issue is fixed, it will print "Issue fixed" and exit with code 0.