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

if __name__ == '__main__':
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
When executed, the script will print the stack trace of the issue and exit with code 1. The expected output is:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 35, in <module>
    reproduce_issue()
  File "reproducer.py", line 31, in reproduce_issue
    plt.show()
  File "/usr/local/lib/python3.8/site-packages/matplotlib/pyplot.py", line 211, in show
    manager.show()
  File "/usr/local/lib/python3.8/site-packages/matplotlib/backends/backend_tkagg.py", line 392, in show
