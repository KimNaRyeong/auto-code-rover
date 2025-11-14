Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
import sys
import traceback

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

def reproduce_bug():
    try:
        import matplotlib
        import matplotlib.pyplot as plt
        import numpy as np

        arr = np.arange(100).reshape((10, 10))

        matplotlib.rcParams['figure.constrained_layout.use'] = True

        fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                          layout='compressed')

        for key in ["B", "C"]:
            ax_dict[key].imshow(arr)

        fig.savefig(StringIO(), bbox_inches="tight")
        fig.savefig(StringIO(), bbox_inches="tight")

    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

reproduce_bug()
```

This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue.