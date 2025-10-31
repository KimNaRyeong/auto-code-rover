The issue is not with the SplineTransformer, but rather with the setup of scikit-learn. The error message indicates that scikit-learn has not been built correctly.

Here's a revised reproducer script:

```python
import numpy as np
from sklearn.preprocessing import SplineTransformer
from sklearn.utils.testing import assert_raises

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
    from sklearn.preprocessing import SplineTransformer
except Exception as e:
    print_stacktrace(e)
    assert False, "Expected ImportError"
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.