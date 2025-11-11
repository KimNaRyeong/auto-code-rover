Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from functools import wraps

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

def assert_raises(func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception")
    except Exception as e:
        print_stacktrace(e)
        return

def reproducer():
    plt.rcParams['figure.constrained_layout.use'] = True
    arr = np.arange(100).reshape((10, 10))
    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2], layout='compressed')

    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)

    fig.savefig("test1.png", bbox_inches="tight")
    plt.rcParams['figure.constrained_layout.use'] = False
    fig.savefig("test2.png", bbox_inches="tight")

    if not (plt.rcParams['figure.constrained_layout.use'] and 'compressed' in str(fig.get_size_inches())):
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    assert_raises(reproducer)
```

This script will run the reproducer function and if the issue is present, it will raise an `AssertionError` with a stack trace.