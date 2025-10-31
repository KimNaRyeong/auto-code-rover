Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from unittest import TestCase
from io import StringIO
from contextlib import redirect_stdout

class Reproducer(TestCase):
    def test_bug(self):
        try:
            # Set up the plot
            arr = np.arange(100).reshape((10, 10))
            fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2], layout='compressed')

            for key in ["B", "C"]:
                ax_dict[key].imshow(arr)

            # Save the first figure
            with StringIO() as f:
                with redirect_stdout(f):
                    fig.savefig("test1.png", bbox_inches="tight")
            self.assertEqual(f.getvalue(), "")

            # Reset the rcParams
            plt.rcParams['figure.constrained_layout.use'] = False

            # Save the second figure
            with StringIO() as f:
                with redirect_stdout(f):
                    fig.savefig("test2.png", bbox_inches="tight")
            if "Compressed layout is not applied" in f.getvalue():
                raise AssertionError("Issue reproduced")
        except Exception as e:
            print_stacktrace(e)
            self.fail()

    def print_stacktrace(self, e: Exception):
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

if __name__ == "__main__":
    Reproducer().test_bug()
```

This script will run the test and if the issue is reproduced, it will raise an `AssertionError` with a stack trace.