Here is the reproducer script:

```python
import numpy as np
from scipy.interpolate import interp1d

def interpolate(y, x):
    return interp1d(range(1, len(y)+1), y)(x)

y = (18, 25, 43, 70, 115)
assert not np.isnan(interpolate(y, 5)), "interpolate could provide value instead of nan"

try:
    interpolate(y, 5)
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

You can run this script with `python3 reproducer.py` to reproduce the issue.