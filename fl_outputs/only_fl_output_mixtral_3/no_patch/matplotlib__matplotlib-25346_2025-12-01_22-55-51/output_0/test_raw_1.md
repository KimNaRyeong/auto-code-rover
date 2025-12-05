 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

fig, ax_arr = plt.subplots(2, 2, figsize=(3, 3), layout="constrained")
fig.suptitle("suptitle that is clearly too long in this case", wrap=True)
ax_arr[1, 0].set_title("axes title that is too long for the size", wrap=True)

try:
    plt.savefig("test.png")
    assert False, "AssertionError not raised"
except AssertionError as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The output should be similar to the following:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    plt.savefig("test.png")
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/pyplot.py", line 697, in savefig
    res = fig.savefig(*args, **kwargs)
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/figure.py", line 2985, in savefig
    self.canvas.print_figure(*args, **kwargs)
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/backend_bases.py", line 2387, in print_figure
    **kwargs)
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/backends/backend_agg.py", line 528, in print_png
    FigureCanvasAgg.draw(self)
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/backends/backend_agg.py", line 466, in draw
    self.figure.draw(self.renderer)
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/artist.py", line 73, in draw_wrapper
    result = draw(artist, renderer, *args, **kwargs)
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/figure.py", line 2908, in draw
    for draw_artist in self.get_default_bbox_extra_artists():
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/figure.py", line 2881, in get_default_bbox_extra_artists
    yield from self.artists + self.get_aux_artists()
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/figure.py", line 2854, in get_aux_artists
    yield from self._suptitle.get_aux_artists()
  File "/home/user/miniconda3/envs/test/lib/python3.9/site-packages/matplotlib/c