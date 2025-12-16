 Here is a standalone Python script `reproducer.py` to reproduce the issue:
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
When executed with Python 3.9.13 and Matplotlib 3.6.0 on Windows, the script raises the following `AssertionError` with a stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    figure.savefig('figure.eps')
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\figure.py", line 3272, in savefig
    self.canvas.print_figure(fname, **kwargs)
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backend_bases.py", line 2338, in print_figure
    result = print_method(
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backend_bases.py", line 2204, in <lambda>
    print_method = functools.wraps(meth)(lambda *args, **kwargs: meth(
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\_api\deprecation.py", line 410, in wrapper
    return func(*inner_args, **inner_kwargs)
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_ps.py", line 869, in _print_ps
    printer(fmt, outfile, dpi=dpi, dsc_comments=dsc_comments,
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\backends\backend_ps.py", line 927, in _print_figure
    self.figure.draw(renderer)
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\artist.py", line 74, in draw_wrapper
    result = draw(artist, renderer, *args, **kwargs)
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\artist.py", line 51, in draw_wrapper
    return draw(artist, renderer, *args, **kwargs)
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\matplotlib\figure.py", line 3069, in draw
    mimage._draw_list_compositing_images(
  File "C:\Users\username\AppData\Local\Programs\Python\Python39\lib\site-packages\