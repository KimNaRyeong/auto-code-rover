Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                             [  2.3e-03,   1.3e-03,   1.8e-02],
                             [  3.3e-03,   2.3e-03,   2.4e-02]]

my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
cm.register_cmap(name='my_cmap_name', cmap=my_cmap)

plt.set_cmap('my_cmap_name')
try:
    plt.imshow([[1, 1], [2, 2]])
except ValueError as e:
    print_stacktrace(e)
    assert False, "Colormap name handling is broken"
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

You can run this script using `python3 reproducer.py`.