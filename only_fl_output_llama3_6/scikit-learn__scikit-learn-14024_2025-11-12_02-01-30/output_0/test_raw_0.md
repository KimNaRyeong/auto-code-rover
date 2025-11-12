Here is the reproducer script:

```python
import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.model_selection import cross_val_score
from sklearn.experimental import enable_hist_gradient_boosting

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
    bunch = fetch_openml(data_id=1491)
    X = bunch.data
    y = bunch.target

    res = cross_val_score(HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=5), X, y)
    np.mean(res)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
```

This script will reproduce the issue and print a stack trace. If you run this script and it doesn't raise an `AssertionError`, then the issue is likely fixed.