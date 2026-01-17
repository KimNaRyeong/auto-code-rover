 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import matplotlib
import sys

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

try:
    # This should raise a KeyError
    cmap = matplotlib.colormaps[None]
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)

# This should not be executed
assert False
```
When executed with `python3 reproducer.py`, the script should print the following stack trace and exit with code 0:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    cmap = matplotlib.colormaps[None]
KeyError: 'None is not a known colormap name'
```
This script demonstrates that accessing `matplotlib.colormaps[None]` raises a `KeyError`, which is the issue reported in the GitHub issue. The proposed solution is to have `matplotlib.colormaps[None]` default to `matplotlib.rcParams['image.cmap']`, which would require modifying the `matplotlib` source code. Alternatively, the documentation could be improved to better explain how to handle this case.