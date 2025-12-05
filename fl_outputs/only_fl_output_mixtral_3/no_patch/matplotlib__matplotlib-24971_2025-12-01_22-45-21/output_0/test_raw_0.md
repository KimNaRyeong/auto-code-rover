 Here is a standalone python script `reproducer.py` to reproduce the issue:

```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np


def print_stacktrace(e: Exception):
    import traceback    import sys
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
    try:
        fig.savefig("test2.png", bbox_inches="tight")
    except Exception as e:
        print_stacktrace(e)
        raise e


if __name__ == "__main__":
    main()
```

This script reproduces the issue and raises an `AssertionError` with a stack trace when executed with `python3 reproducer.py`. The line numbers of the statements should be shown clearly in the stack trace.