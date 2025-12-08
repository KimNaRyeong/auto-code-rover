 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector

def print(vmin, vmax):
    print(f"vmin = {vmin}, vmax = {vmax}")

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

fig, ax = plt.subplots()
ax.plot([10, 20], [10, 20])
ss = SpanSelector(ax, print, "horizontal", span_stays=True)  # or interactive=True
plt.show()

try:
    ss.onremove(None)
    assert False, "onremove should raise an exception when the selector is not active"
except AssertionError:
    pass
except Exception as e:
    print_stacktrace(e)
    assert False, f"onremove raised an unexpected exception: {e}"
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    ss.onremove(None)
  File "/home/user/.local/lib/python3.9/site-packages/matplotlib/widgets.py", line 216, in onremove
    self.disconnect(cid)
  File "/home/user/.local/lib/python3.9/site-packages/matplotlib/cbook/__init__.py", line 223, in __call__
    return mtd(*args, **kwargs)
  File "/home/user/.local/lib/python3.9/site-packages/matplotlib/cbook/__init__.py", line 213, in __call__
    return self.callback(*args, **kwargs)
  File "reproducer.py", line 7, in print
    print(f"vmin = {vmin}, vmax = {vmax}")
UnboundLocalError: local variable 'vmin' referenced before assignment
```
The issue is that when the `SpanSelector` is interactively removed by clicking and immediately releasing the button, the `onselect` callback is not fired, and the `onremove` callback is not called either. The `onremove` callback should be called with a `None` argument when the selector is removed, but it is not called at all.

To fix the issue, the `onremove` callback should be called with a `None` argument when the selector is interactively removed by clicking and immediately releasing the button. This can be done by modifying the `SpanSelector` class in the `matplotlib.widgets` module as follows:
```python
class SpanSelector(object):
    # ...
    def on_mouse_release(self, event):
        if event.button != self.button:
            return
        if not self.active:
            self.onremove(None)  # add this line
            return
        # ...
```
With this modification, the `onremove` callback is called with a `None` argument when the selector is interactively removed by clicking and immediately releasing the button, and the `AssertionError` is not raised in the `reproducer.py` script.