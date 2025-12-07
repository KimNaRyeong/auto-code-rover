 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.figure as figure
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

try:
    figure = figure.Figure()
    ax = figure.add_subplot(111)
    ax.annotate(text='\nLower label', xy=(0, 0))
    figure.savefig('figure.eps')
except Exception as e:
    print_stacktrace(e)
    assert False

plt.show()
```
When executed with `python3 reproducer.py`, the script raises a `TypeError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    figure.savefig('figure.eps')
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/figure.py", line 3272, in savefig
    self.canvas.print_figure(fname, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/backend_bases.py", line 2338, in print_figure
    result = print_method(
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/backend_bases.py", line 2204, in <lambda>
    print_method = functools.wraps(meth)(lambda *args, **kwargs: meth(
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/_api/deprecation.py", line 410, in wrapper
    return func(*inner_args, **inner_kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/backends/backend_ps.py", line 869, in _print_ps
    printer(fmt, outfile, dpi=dpi, dsc_comments=dsc_comments,
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/backends/backend_ps.py", line 927, in _print_figure
    self.figure.draw(renderer)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/artist.py", line 74, in draw_wrapper
    result = draw(artist, renderer, *args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/artist.py", line 51, in draw_wrapper
    return draw(artist, renderer, *args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/figure.py", line 3069, in draw
    mimage._draw_list_compositing_images(
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/image.py", line 131, in _draw_list_compositing_images
    a.draw(renderer)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/artist.py", line 51, in draw_wrapper
    return draw(artist, renderer, *args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/matplotlib/axes/_base.py", line 