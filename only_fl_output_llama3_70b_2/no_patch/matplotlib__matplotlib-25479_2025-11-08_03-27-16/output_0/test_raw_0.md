Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap
import matplotlib.pyplot as plt

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                             [  2.3e-03,   1.3e-03,   1.8e-02],
                             [  3.3e-03,   2.3e-03,   2.4e-02]]

my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
cm.register_cmap(name='my_cmap_name', cmap=my_cmap)

try:
    plt.set_cmap('my_cmap_name')
    plt.imshow([[1, 1], [2, 2]])
except ValueError as e:
    print_stacktrace(e)
    assert False, "Colormap 'some_cmap_name' is not recognized"
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

To execute the script, run `python3 reproducer.py` in the terminal.