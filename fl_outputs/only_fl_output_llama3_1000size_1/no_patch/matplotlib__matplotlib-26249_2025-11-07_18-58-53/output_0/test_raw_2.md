I apologize for the mistake earlier. Here is a new reproducer script that should reproduce the issue:

```python
import numpy as np
from matplotlib import pyplot as plt

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
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter([1,np.nan,3], [2,np.nan,4], [3, np.nan,5], color=[[.5,.5,.5,.5]]*3, s=11.5)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue not fixed")
finally:
    plt.show()
```

This script should reproduce the issue and then exit with code 0 if the issue is fixed.