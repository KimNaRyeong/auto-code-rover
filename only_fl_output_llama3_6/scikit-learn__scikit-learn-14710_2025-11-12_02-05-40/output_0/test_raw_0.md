Here is the reproducer script for the issue:

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
    X = np.random.randn(100, 10)
    y = np.array(['x'] * 50 + ['y'] * 50, dtype=object)
    gbrt = HistGradientBoostingClassifier(n_iter_no_change=10)
    gbrt.fit(X, y)
except Exception as e:
    print_stacktrace(e)
    raise
```

This script will attempt to reproduce the issue by creating a random dataset and fitting a `HistGradientBoostingClassifier` with early stopping. If an exception is raised during this process, it will be caught and printed using the provided `print_stacktrace` function before re-raising it.