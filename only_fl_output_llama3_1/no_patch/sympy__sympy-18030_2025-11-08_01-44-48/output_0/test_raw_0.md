Here is the reproducer script:

```python
import numpy as np

def interpolate(y, x):
    from scipy.interpolate import interp1d
    
    f = interp1d(np.arange(1, len(y)+1), y)
    return f(x)

y = (18, 25, 43, 70, 115)
try:
    result = interpolate(y, 5)
    assert not np.isnan(result)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.