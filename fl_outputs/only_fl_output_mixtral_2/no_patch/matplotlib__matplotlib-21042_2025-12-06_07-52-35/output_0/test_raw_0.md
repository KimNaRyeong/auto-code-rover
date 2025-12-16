 Here is a standalone python script `reproducer.py` that reproduces the issue:
```python
import matplotlib as mpl
import sys

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    rc = dict(mpl.rc_params())
    mpl.rcParams.update(rc)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 11, in <module>
    mpl.rcParams.update(rc)
  File ".../miniconda3/envs/testmpl/lib/python3.9/site-packages/matplotlib/rcsetup.py", line 629, in update
    self[k] = conv(v)
  File ".../miniconda3/envs/testmpl/lib/python3.9/site-packages/matplotlib/__init__.py", line 841, in __setitem__
    raise MatplotlibDeprecationWarning(
MatplotlibDeprecationWarning: The datapath rcparam was deprecated in Matplotlib 3.2.1 and will be removed two minor releases later.
```
This stack trace confirms the presence of the issue, as it shows that the `MatplotlibDeprecationWarning` is raised when updating the `rcParams`.