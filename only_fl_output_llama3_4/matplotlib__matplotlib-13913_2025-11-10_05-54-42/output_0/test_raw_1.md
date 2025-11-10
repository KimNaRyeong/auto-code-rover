Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors

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
    c = np.arange(1000).astype(str)
    X = np.random.normal(0, 1, [1000, 2])

    assert all([colors.is_color_like(color) for color in c])
    plt.scatter(X[:, 0], X[:, 1], c=c)

except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script should reproduce the issue and raise an `AssertionError` when the issue is present.