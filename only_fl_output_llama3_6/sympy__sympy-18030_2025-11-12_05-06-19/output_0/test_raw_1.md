Here is the reproducer script:

```python
import scipy.interpolate as si
from scipy import interpolate

def interpolate(y, x):
    f = interpolate.interp1d(range(1, len(y)+1), y)
    return f(x)

y = (18,25,43,70,115)
try:
    result = interpolate(y, 5)
    assert not np.isnan(result), "Expected a value instead of nan"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` if the issue is present and print the stack trace. If the issue is fixed, it will simply exit with code 0.