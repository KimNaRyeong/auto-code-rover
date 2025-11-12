Here is the reproducer script:

```python
import numpy as np

def interpolate(y, x):
    f = np.interp(x, range(1, len(y)+1), y)
    return f

y = (18,25,43,70,115)
try:
    result = interpolate(5, y)
    assert not np.isnan(result), "Expected a value instead of nan"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully")
exit(0)
```

This script will raise an `AssertionError` if the issue is present and print the stack trace. If the issue is fixed, it will simply print "Issue reproduced successfully" and exit with code 0.