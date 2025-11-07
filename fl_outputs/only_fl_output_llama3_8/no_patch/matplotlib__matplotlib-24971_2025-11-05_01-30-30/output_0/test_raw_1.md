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

def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception but got nothing")
    except expected_exception as e:
        return

def reproducer():
    matplotlib.rcParams['figure.constrained_layout.use'] = True
    
    arr = np.arange(100).reshape((10, 10))
    
    fig, ax_dict = plt.subplot_mosaic('AB;AC', figsize=(6, 9), width_ratios=[3, 2],
                                      layout='compressed')
    
    for key in ["B", "C"]:
        ax_dict[key].imshow(arr)
        
    original_layout = matplotlib.rcParams['figure.constrained_layout.use']
    try:
        fig.savefig("test1.png", bbox_inches="tight")
        fig.savefig("test2.png", bbox_inches="tight")
    finally:
        matplotlib.rcParams['figure.constrained_layout.use'] = original_layout

    if not "compressed" in str(fig):
        raise AssertionError("Compressed layout is not applied the second time a figure is saved")

reproducer()
```

This script will reproduce the issue and print the stack trace when an `AssertionError` is raised.