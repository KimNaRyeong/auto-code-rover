Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from unittest import TestCase
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

class Reproducer(TestCase):
    def test_reproducer(self):
        matplotlib.rcParams['figure.constrained_layout.use'] = True

        arr = np.arange(100).reshape((10, 10))

        fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                            layout='compressed')

        for key in ["B", "C"]:
            ax_dict[key].imshow(arr)

        with open("test1.png", "w") as f:
            fig.savefig(f, bbox_inches="tight")

        matplotlib.rcParams['figure.constrained_layout.use'] = False

        with open("test2.png", "w") as f:
            fig.savefig(f, bbox_inches="tight")

        if not (plt.imread("test1.png").shape == plt.imread("test2.png").shape):
            raise AssertionError("Compressed layout setting can be forgotten on second save")
        else:
            print("Issue fixed")

if __name__ == "__main__":
    try:
        Reproducer().test_reproducer()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```

This script will raise an `AssertionError` if the compressed layout setting is forgotten on the second save, and it will print a stack trace of the issue. If the issue is fixed, it will exit with code 0.