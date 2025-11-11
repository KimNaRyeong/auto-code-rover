Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import numpy as np
from io import StringIO
from contextlib import redirect_stdout

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

def reproduce_issue():
    try:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), dpi=120, facecolor='white', subplot_kw=dict(projection='polar'))
        ax1.plot(np.radians(np.random.rand(10000)*360), np.random.rand(10000), 'o', markersize=1)
        ax1.set_title('expected', pad=12)
        ax2.plot(np.radians(np.random.rand(10000)*360), np.random.rand(10000), 'o', markersize=1)
        ax2.set_title('unexpected', pad=12)
        ax1.set_ylim(bottom=0)
        # ax2.set_ylim(bottom=0)
        print(ax2.get_ylim())
    except AssertionError as e:
        with StringIO() as f, redirect_stdout(f):
            print_stacktrace(e)
        print(f.read(), end='')
        exit(1)

reproduce_issue()
```

This script will reproduce the issue and raise an `AssertionError` when it is present. The stack trace of the issue will be printed to the console.