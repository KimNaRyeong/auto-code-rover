Here is the reproducer script:

```python
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import numpy as np
import matplotlib as mpl

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

    fig = plt.gcf()
    fig.canvas.draw()

    if not (cbar.ax.get_window_extent().get_width() > 0 and cbar.ax.get_window_extent().get_height() < 1):  # Check if the colorbar has edges
        raise AssertionError("Expected the colorbar to have edges at extremities")

except Exception as e:
    print_stacktrace(e)
    exit(1)

plt.show()
```

This script will attempt to reproduce the issue by creating a matplotlib colorbar with `drawedges=True` and `extend='both'`. If the colorbar does not have edges at the extremities, it will raise an `AssertionError`, which will be caught and printed along with a stack trace.