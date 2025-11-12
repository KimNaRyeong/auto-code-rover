Here is the reproducer script:

```python
import seaborn
from packaging import version

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    import matplotlib
    LooseVersion = version.LooseVersion

    import seaborn
    from .rcmod import *  # noqa: F401,F403

except DeprecationWarning as e:
    print_stacktrace(e)
    raise AssertionError("DeprecationWarning: distutils Version classes are deprecated. Use packaging.version instead.")
```

This script will attempt to import `seaborn`, then use the `LooseVersion` class from it, and finally import `matplotlib`. If a `DeprecationWarning` is raised, the script will print the stack trace using the provided function and then raise an `AssertionError`.