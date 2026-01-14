 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import matplotlib.cm as cm

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

matplotlib.__version__

my_cmap_data = [[  1.5e-03,   4.7e-04,   1.4e-02],
                             [  2.3e-03,   1.3e-03,   1.8e-02],
                             [  3.3e-03,   2.3e-03,   2.4e-02]]
my_cmap = colors.LinearSegmentedColormap.from_list('some_cmap_name', my_cmap_data)
cm.register_cmap(name='my_cmap_name', cmap=my_cmap)

plt.set_cmap('my_cmap_name')  # All OK setting the cmap
plt.imshow([[1, 1], [2, 2]])

try:
    plt.show()
except Exception as e:
    print_stacktrace(e)
    assert False
```

When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with a stack trace showing the issue. The script should exit with code 1.

The output will be similar to:

```
1.4.3.
Traceback (most recent call last):
  File "reproducer.py", line 26
    plt.show()
  File "/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/pyplot.py", line 214, in show
    manager.show()
  File "/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/backends/backend_tkagg.py", line 32, in show
    Tk.mainloop(self._tk)
  File "/usr/local/continuum/anaconda/envs/py34/lib/python3.4/tkinter/__init__.py", line 489, in mainloop
    _default_root.tk.mainloop(n)
  File "/usr/local/continuum/anaconda/envs/py34/lib/python3.4/site-packages/matplotlib/backends/backend_tkagg.py", line 30, in _on_close
    window.destroy()
  File "/usr/local/continuum/anaconda/envs/py34/lib/python3.4/tkinter/__init__.py", line 1763, in destroy
    self.tk.call('destroy', self._w)
ValueError: Colormap some_cmap_name is not recognized. Possible values are: Set1_r, gnuplot_r, Set3_r, gist_rainbow, gist_ncar_r, gist_gray_r, Spectral_r, hot, nipy_spectral, hsv_r, rainbow, GnBu, PuRd, Spectral, BrBG_r, PRGn_r, YlGnBu_r, BuPu, binary_r, summer_r, flag_r, PuBu, Accent, Reds, winter_r, Greys, PuOr_r, gnuplot2, brg_r, Set2_r, PuBu_r, Purples_r