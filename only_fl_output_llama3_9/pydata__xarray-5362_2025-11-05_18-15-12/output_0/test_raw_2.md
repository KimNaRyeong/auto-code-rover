The issue is not related to the weighted operations in xarray, but rather with the numpy version. The error message indicates that `np.unicode_` was removed in the NumPy 2.0 release and you should use `np.str_` instead.

Here's a simple reproducer script:

```python
import numpy as np

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
    np.unicode_
except AttributeError as e:
    print_stacktrace(e)
    raise AssertionError("Expected an error")
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.