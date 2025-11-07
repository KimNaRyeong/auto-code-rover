Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import sys

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
    import matplotlib
    matplotlib.rcParams['figure.constrained_layout.use'] = True

    arr = np.arange(100).reshape((10, 10))

    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                        layout='compressed')

    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)

    fig.savefig("test1.png")
    fig.savefig("test2.png")

    if not (plt.imread("test1.png") == plt.imread("test2.png")).all():
        raise AssertionError("Compressed layout setting can be forgotten on second save")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script will reproduce the issue by saving two figures with compressed layout. If the images are not identical, it will raise an `AssertionError` and print a stack trace of the issue.