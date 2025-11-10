Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
import numpy as np
from matplotlib import pylab as plt
import sys
import traceback

def print_stacktrace(e: Exception):
    print("Traceback (most recent call last):", file=sys.stderr)
    tb = traceback.extract_tb(e.__traceback__)
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
    sys.exit(1)

sys.exit(0)
```

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise an error and print a stack trace.