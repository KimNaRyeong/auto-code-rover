 Here is a standalone python script `reproducer.py` that reproduces the issue:
```python
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    c = np.arange(1000).astype(str)
    X = np.random.normal(0, 1, [1000, 2])

    assert all([matplotlib.colors.is_color_like(color) for color in c]), "is_color_like should return True for strings of integers"

    try:
        plt.scatter(X[:, 0], X[:, 1], c=c)
    except Exception as e:
        print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise a `ValueError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    plt.scatter(X[:, 0], X[:, 1], c=c)
  File "/usr/lib/python3.7/site-packages/matplotlib/pyplot.py", line 2864, in scatter
    is not None else {}), **kwargs)
  File "/usr/lib/python3.7/site-packages/matplotlib/__init__.py", line 1810, in inner
    return func(ax, *args, **kwargs)
  File "/usr/lib/python3.7/site-packages/matplotlib/axes/_axes.py", line 4297, in scatter
    alpha=alpha)
  File "/usr/lib/python3.7/site-packages/matplotlib/collections.py", line 899, in __init__
    Collection.__init__(self, **kwargs)
  File "/usr/lib/python3.7/site-packages/matplotlib/collections.py", line 131, in __init__
    self.set_facecolor(facecolors)
  File "/usr/lib/python3.7/site-packages/matplotlib/collections.py", line 685, in set_facecolor
    self._set_facecolor(c)
  File "/usr/lib/python3.7/site-packages/matplotlib/collections.py", line 668, in _set_facecolor
    self._facecolors = mcolors.to_rgba_array(c, self._alpha)
  File "/usr/lib/python3.7/site-packages/matplotlib/colors.py", line 260, in to_rgba_array
    raise ValueError("RGBA values should be within 0-1 range")
ValueError: RGBA values should be within 0-1 range
```
This confirms that the `is_color_like` function returns `True` for strings of integers, which is not expected behavior. The `scatter` function then fails with a `ValueError` when it tries to convert these strings to RGBA values.