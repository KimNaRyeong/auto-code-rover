I apologize for the mistake earlier. Here is a new reproducer script that should correctly reproduce the issue:

```python
import matplotlib.pyplot as plt
from matplotlib.colors import from_levels_and_colors
import numpy as np
import sys
import traceback

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
    my_cmap = plt.cm.get_cmap('viridis')
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(0, 1, nb_colors))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

    fig = plt.figure(figsize=(5, 1))
    ax = fig.add_subplot(111)
    cbar = plt.colorbar(ax=ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)

    if not (cbar.ax.get_ybound()[0] == 0 and cbar.ax.get_ybound()[1] == 1):
        raise AssertionError("Expected edges at extremities")

except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```

This script will create a color bar with `drawedges=True` and `extend='both'`, then check if the edges are drawn at the extremities. If they are not, it will raise an `AssertionError`.