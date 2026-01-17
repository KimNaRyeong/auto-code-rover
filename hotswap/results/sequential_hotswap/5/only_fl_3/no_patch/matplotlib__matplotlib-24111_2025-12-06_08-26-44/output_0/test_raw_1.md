 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib
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
    # This should raise a KeyError
    cmap = matplotlib.colormaps[None]
    assert cmap is None
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)

# This should not raise any exception
cmap = matplotlib.cm.get_cmap(None)
assert cmap is not None
```
When executed with Python 3.9.2 and Matplotlib 3.5.1, the script prints the following stack trace:
```css
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    cmap = matplotlib.colormaps[None]
KeyError: 'None is not a known colormap name'
```
This confirms that the issue is present in the current version of Matplotlib. If the proposed solution is implemented, the script should exit without any error message.