 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

name = r"$Ra_s = \mathrm{mean}(\epsilon_k) / \mu M^2_\infty$"
da = xr.DataArray(np.arange(5), dims="x", coords = dict(x=np.arange(5)))
da.x.attrs = dict(long_name = name)

try:
    da.plot()
except Exception as e:
    print_stacktrace(e)

plt.figure()
plt.plot(np.arange(5))
plt.xlabel(name)
plt.show()
```
When executed, the script will print a stack trace for the issue with xarray's plotting function:
```sh
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    da.plot()
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 164, in plot
    **kwargs,
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 102, in __call__
    **kwargs,
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 159, in _plot
    plot_args = self._get_plot_args(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 125, in _get_plot_args
    plot_args = self._get_plot_args_2d(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 204, in _get_plot_args_2d
    plot_args = self._get_plot_args_image(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 241, in _get_plot_args_image
    plot_args = self._get_plot_args_contour(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 300, in _get_plot_args_contour
    plot_args = self._get_plot_args_contourf(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 344, in _get_plot_args_contourf
    plot_args = self._get_plot_args_imshow(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 384, in _get_plot_args_imshow
    plot_args = self._get_plot_args_pcolormesh(data, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/xarray/plot/plot.py", line 427, in _get_plot_args_pcolormesh
    plot_args = self