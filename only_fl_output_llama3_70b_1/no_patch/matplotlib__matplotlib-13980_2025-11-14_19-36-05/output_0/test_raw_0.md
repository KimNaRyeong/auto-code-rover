Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
import numpy as np
import random

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

npoints = 10_000
theta = 360 * np.random.rand(npoints)
r = np.random.rand(npoints)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 4), dpi=120, facecolor='white', subplot_kw=dict(projection='polar'))
ax1.plot(np.radians(theta), r, 'o', markersize=1)
ax1.set_title('expected', pad=12)
ax2.plot(np.radians(theta), r, 'o', markersize=1)
ax2.set_title('unexpected', pad=12)
ax1.set_ylim(bottom=0)

try:
    assert ax2.get_ylim()[0] >= 0
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

plt.show()
```
This script reproduces the issue by creating a polar plot with random data and checking if the minimum y-limit is non-negative. If it's not, an `AssertionError` is raised, printing the stack trace of the issue.