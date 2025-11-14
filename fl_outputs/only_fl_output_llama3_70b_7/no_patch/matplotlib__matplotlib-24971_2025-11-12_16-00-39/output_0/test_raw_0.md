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

def main():
    arr = np.arange(100).reshape((10, 10))

    matplotlib.rcParams['figure.constrained_layout.use'] = True

    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                      layout='compressed')

    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)

    fig.savefig("test1.png", bbox_inches="tight")
    fig.savefig("test2.png", bbox_inches="tight")

    # Check if the issue is present
    with open("test1.png", "rb") as f1, open("test2.png", "rb") as f2:
        if f1.read() != f2.read():
            raise AssertionError("Compressed layout setting is forgotten on second save")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
```
This script reproduces the issue by creating two figures with compressed layout and saving them twice. It then checks if the resulting images are identical, and raises an `AssertionError` if they are not. If the issue is present, it prints a stack trace of the error and exits with code 1. If the issue is fixed, it exits with code 0.