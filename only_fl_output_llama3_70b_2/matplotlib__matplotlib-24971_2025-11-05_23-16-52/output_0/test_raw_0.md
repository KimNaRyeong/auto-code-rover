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

try:
    arr = np.arange(100).reshape((10, 10))

    matplotlib.rcParams['figure.constrained_layout.use'] = True

    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                      layout='compressed')

    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)

    fig.savefig("test1.png", bbox_inches="tight")
    fig.savefig("test2.png", bbox_inches="tight")

    # Check if the images are identical
    with open("test1.png", "rb") as f1, open("test2.png", "rb") as f2:
        img1 = f1.read()
        img2 = f2.read()

    assert img1 == img2, "Images are not identical"

except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script reproduces the issue by saving two images with `bbox_inches="tight"` and checking if they are identical. If the images are not identical, it raises an `AssertionError` and prints a stack trace of the issue using the provided `print_stacktrace` function.