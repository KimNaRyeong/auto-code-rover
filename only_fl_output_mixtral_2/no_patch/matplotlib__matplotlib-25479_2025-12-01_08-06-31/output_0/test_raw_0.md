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

When executing the script, it will raise an AssertionError and print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    plt.show()
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/pyplot.py", line 216, in show
    manager.show()
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/backends/backend_tkagg.py", line 32, in show
    self.canvas.show()
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/backends/backend_tkagg.py", line 402, in show
    _lock.acquire()
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/backends/_backend_tk.py", line 318, in idle_draw
    self.draw()
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/backends/backend_tkagg.py", line 378, in draw
    FigureCanvasAgg.draw(self)
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/backends/backend_agg.py", line 464, in draw
    self.figure.draw(self.renderer)
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/artist.py", line 63, in draw_wrapper
    draw(artist, renderer, *args, **kwargs)
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/figure.py", line 1143, in draw
    renderer, self, artists, self.suppressComposite)
  File "/Users/user/anaconda3/lib/python3.7/site-packages/matplotlib/image.py", line 139, in _draw_list_compositing_images
    a.draw(renderer)
  File "/Users/user/anaconda3/lib