Here is the reproducer script:

```python
import numpy as np

def interpolate(y, x):
    from scipy.interpolate import interp1d
    f = interp1d(np.arange(1, len(y)+2), y)
    return f(x)

y = (18,25,43,70,115)
try:
    result = interpolate(y, 5)
    assert np.isnan(result) == False, "Expected a value instead of nan"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` if the issue is present and print the stack trace. If the issue is fixed, it will simply exit with code 0.