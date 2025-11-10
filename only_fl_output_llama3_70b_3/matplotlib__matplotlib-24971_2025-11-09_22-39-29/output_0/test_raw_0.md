Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

arr = np.arange(100).reshape((10, 10))

matplotlib.rcParams['figure.constrained_layout.use'] = True

fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                  layout='compressed')

for key in ["B", "C"]:
    ax_dict[key].imshow(arr)

fig.savefig("test1.png", bbox_inches="tight")
fig.savefig("test2.png", bbox_inches="tight")

try:
    assert plt.imread("test1.png").shape == plt.imread("test2.png").shape
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will reproduce the issue and raise an `AssertionError` if the images are not identical. The `print_stacktrace` function is used to print a detailed stack trace of the error, including line numbers. If the issue is fixed, the script will exit with code 0.