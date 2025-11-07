Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from matplotlib.colors import LinearSegmentedColormap
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    my_cmap_data = [[ 1.5e-03,   4.7e-04,   1.4e-02],
                     [ 2.3e-03,   1.3e-03,   1.8e-02],
                     [ 3.3e-03,   2.3e-03,   2.4e-02]]
    my_cmap = LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
    cm.register_cmap(name='my_cmap_name', cmap=my_cmap)

    plt.set_cmap('my_cmap_name')  # All OK setting the cmap
    plt.imshow([[1, 1], [2, 2]])
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.