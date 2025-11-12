Here is the standalone Python file `reproducer.py` to reproduce the issue:

```python
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
    fig, ax = plt.subplots(1, 2, figsize=(8, 2), constrained_layout=False)
    ax[0].plot(np.linspace(0, 2 * np.pi, 100), np.sin(np.linspace(0, 2 * np.pi, 100)))
    ax[1].plot(np.linspace(0, 2 * np.pi, 100), np.cos(np.linspace(0, 2 * np.pi, 100)))
    plt.subplots_adjust(wspace=0)
except UserWarning as e:
    print_stacktrace(e)
    assert False, "Expected no warning"
else:
    exit(0)