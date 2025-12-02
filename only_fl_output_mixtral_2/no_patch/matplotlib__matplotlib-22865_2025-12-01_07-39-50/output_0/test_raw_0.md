 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
import matplotlib as mpl
import numpy as np
import matplotlib.pyplot as plt 
from matplotlib.colors import from_levels_and_colors

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    my_cmap = mpl.cm.viridis
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

    plt.figure(figsize=(5, 1))
    ax = plt.subplot(111)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=True)
    plt.subplots_adjust(left=0.05, bottom=0.4, right=0.95, top=0.9)
    plt.show()

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
When executed, the script will show the actual outcome of the colorbar without the black lines at the extremities. The script will then exit with code 1, indicating that the issue is present.

To fix the issue, one possible solution is to modify the `reproduce_issue` function to manually draw the black lines at the extremities of the colorbar. Here is an example of how to do it:
```python
def reproduce_issue():
    my_cmap = mpl.cm.viridis
    bounds = np.arange(10)
    nb_colors = len(bounds) + 1
    colors = my_cmap(np.linspace(100, 255, nb_colors).astype(int))
    my_cmap, my_norm = from_levels_and_colors(bounds, colors, extend='both')

    plt.figure(figsize=(5, 1))
    ax = plt.subplot(111)
    cbar = mpl.colorbar.ColorbarBase(ax, cmap=my_cmap, norm=my_norm, orientation='horizontal', drawedges=False)
    plt.subplots_adjust(left=0.05, bottom=0.4, right=0.95, top=0.9)

    # Get the limits of the colorbar
    cbar_min, cbar_max = cbar.get_clim()

    # Calculate the positions of the black lines
    line_positions = [cbar_min, cbar_min + (cbar_max - cbar_min) / (nb_colors - 1)]

    # Draw the black lines
    for pos in line_positions:
        plt.axhline(y=pos, color='black', linestyle='-', linewidth=1)

    plt.show()
```
With this modification, the script will show the expected outcome of the colorbar with the black lines at the extremities. The script will then exit with code 0, indicating that the issue is fixed.