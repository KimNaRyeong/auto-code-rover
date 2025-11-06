The issue is not with the code you provided, but rather with the installation of scikit-learn. It seems that scikit-learn has not been built correctly.

To reproduce this issue, we can create a simple Python script that imports HistGradientBoostingClassifier and tries to use it:

```python
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import HistGradientBoostingClassifier

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
    gb = HistGradientBoostingClassifier(loss='categorical_crossentropy')
except Exception as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace.