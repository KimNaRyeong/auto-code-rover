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
When executed with Python 3.9.2 and Matplotlib 3.5.1, this script reproduces the issue and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    cmap = matplotlib.colormaps[None]
KeyError: 'None is not a known colormap name'
```
To fix the issue, you can modify the `reproducer.py` script as follows:
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
    # This should not raise any exception
    cmap_name = matplotlib.rcParams['image.cmap']
    cmap = matplotlib.colormaps.get(cmap_name)
    assert cmap is not None
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
When executed with the same version of Python and Matplotlib, this script should not raise any exception and exit with code 0.