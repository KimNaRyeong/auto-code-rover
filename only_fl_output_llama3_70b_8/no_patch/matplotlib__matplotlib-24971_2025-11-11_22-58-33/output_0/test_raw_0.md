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

matplotlib.rcParams['figure.constrained_layout.use'] = True

arr = np.arange(100).reshape((10, 10))

fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2], layout='compressed')

for key in ["B", "C"]:
    ax_dict[key].imshow(arr)

fig.savefig("test1.png", bbox_inches="tight")
first_img = plt.imread("test1.png")

fig.savefig("test2.png", bbox_inches="tight")
second_img = plt.imread("test2.png")

try:
    assert np.array_equal(first_img, second_img), "Compressed layout setting is forgotten on the second save"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script will raise an `AssertionError` if the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.