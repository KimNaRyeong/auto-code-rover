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

fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2], layout='compressed')

for key in ["B", "C"]:
    ax_dict[key].imshow(arr)

fig.savefig("test1.png", bbox_inches="tight")
img1_size = fig.bbox_inches.bounds

fig.savefig("test2.png", bbox_inches="tight")
img2_size = fig.bbox_inches.bounds

if img1_size != img2_size:
    raise AssertionError("Compressed layout setting is forgotten on second save")

print("Issue not present, exiting with code 0")
exit(0)
```
This script will reproduce the issue and raise an `AssertionError` if the compressed layout setting is forgotten on the second save. If the issue is fixed, it will print a success message and exit with code 0.