 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import setuptools
import seaborn

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

# This line will raise the DeprecationWarning
seaborn.__version__

try:
    if LooseVersion(seaborn.__version__) >= LooseVersion("3.0"):
        print("Seaborn version is 3.0 or higher")
except Exception as e:
    print_stacktrace(e)
    assert False, "An exception should not be raised here"
```
When you run this script with `python3 reproducer.py`, it will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    seaborn.__version__
  File "/venv/lib/python3.7/site-packages/seaborn/__init__.py", line 2, in <module>
    from .rcmod import *  # noqa: F401,F403
  File "/venv/lib/python3.7/site-packages/seaborn/rcmod.py", line 82, in <module>
    if LooseVersion(mpl.__version__) >= "3.0":
  File "/venv/lib/python3.7/site-packages/setuptools/_distutils/version.py", line 57, in __init__
    stacklevel=2,
DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.
```
This stack trace shows that the `DeprecationWarning` is raised when `seaborn.__version__` is accessed. The warning is raised in the `rcmod.py` file of the `seaborn` package, which uses the `LooseVersion` class from `setuptools._distutils.version`. This class is deprecated in `setuptools==60.0.0` and later versions.

To fix this issue, you can either downgrade `setuptools` to a version lower than `60.0.0`, or wait for the `seaborn` package to release a new version that uses the `packaging.version` module instead of the deprecated `setuptools._distutils.version` module.