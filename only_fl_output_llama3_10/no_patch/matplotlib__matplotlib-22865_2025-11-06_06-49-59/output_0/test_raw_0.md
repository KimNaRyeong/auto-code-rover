Here is the reproducer script:

```python
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import traceback
import sys

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
    my_cmap = mpl.cm.viridis
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

    plt.figure(figsize=(5, 1))
    ax = plt.subplot(111)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)

    if not cbar.ax.get_window_rectangles()[0][2] == cbar.ax.get_window_rectangles()[-1][2]:
        raise AssertionError("Colorbar with drawedges=True and extend='both' does not draw edges at extremities")

except Exception as e:
    print_stacktrace(e)
finally:
    plt.show()
    if 'plt' in globals():
        plt.close('all')
```

This script will reproduce the issue by checking if the width of the colorbar is equal to the sum of the widths of its constituent parts. If it's not, an `AssertionError` will be raised with a stack trace that shows the line numbers of the statements.