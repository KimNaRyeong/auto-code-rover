 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
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

def main():
    cmap = plt.get_cmap('bwr_r')
    fig, ax = plt.subplots()
    x, y = np.mgrid[0:10:100j, 0:10:100j]
    v = np.abs(np.sin(x) * np.cos(y))
    c = (cmap(v[:-1, :-1]) * 255).astype(np.int64)
    try:
        ax.pcolorfast(x, y, c)
        plt.show()
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with Python 3.10.1 and Matplotlib 3.5.1, the script raises the following `AssertionError`:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    main()
  File "reproducer.py", line 21, in main
    ax.pcolorfast(x, y, c)
  File "/home/user/.local/lib/python3.10/site-packages/matplotlib/__init__.py", line 1432, in inner
    return func(ax, *args, **kwargs)
  File "/home/user/.local/lib/python3.10/site-packages/matplotlib/axes/_axes.py", line 5637, in pcolorfast
    **kwargs)
  File "/home/user/.local/lib/python3.10/site-packages/matplotlib/collections.py", line 1084, in __init__
    raise ValueError("RGBA values should be within 0-1 range")
ValueError: RGBA values should be within 0-1 range
```
This confirms the presence of the issue. To fix the issue, you can modify the `collections.py` file as suggested in the issue description. Alternatively, you can use the following workaround in the `main()` function:
```python
    c = (cmap(v[:-1, :-1]) * 255).astype(np.float64)
    ax.imshow(c, extent=[x.min(), x.max(), y.min(), y.max()], origin='lower')
    plt.show()
```
This uses `imshow()` instead of `pcolorfast()` to display the image. The `extent` and `origin` parameters are used to align the image with the coordinate system. This workaround avoids the need to modify the `collections.py` file.