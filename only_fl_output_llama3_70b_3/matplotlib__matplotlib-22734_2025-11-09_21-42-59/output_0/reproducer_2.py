import numpy as np
import matplotlib.pyplot as plt

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
    from pylab import *
    tripcolor(np.random.rand(100), np.random.rand(100), np.random.rand(100), clim=(0, 0.5))
    colorbar = plt.colorbar()
    vmin, vmax = colorbar.ax.get_ylim()
    assert not np.allclose((vmin, vmax), (0, 0.5)), "tripcolor does not ignore clim"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

plt.show()
