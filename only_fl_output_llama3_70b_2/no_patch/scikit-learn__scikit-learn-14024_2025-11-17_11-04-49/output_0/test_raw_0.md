Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
# reproducer.py

import numpy as np
from sklearn.datasets import fetch_openml
from sklearn.model_selection import cross_val_score
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
    # Load dataset
    bunch = fetch_openml(data_id=1491)
    X = bunch.data
    y = bunch.target

    # Train HistGradientBoostingClassifier
    clf = HistGradientBoostingClassifier(max_iter=100, min_samples_leaf=5)
    res = cross_val_score(clf, X, y)

    # Check if result is NaN
    if np.isnan(np.mean(res)):
        raise AssertionError("Zero division error in HistGradientBoosting")
except Exception as e:
    print_stacktrace(e)
    exit(1)
```
<|start_header_id|>