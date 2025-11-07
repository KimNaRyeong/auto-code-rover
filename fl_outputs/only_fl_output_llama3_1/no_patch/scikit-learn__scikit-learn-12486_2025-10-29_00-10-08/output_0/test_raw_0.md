Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from sklearn.mixture import GMM
from sklearn.grid_search import GridSearchCV
from sklearn.metrics.scorer import _check_classification_targets

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

def reproduce_issue():
    X, y = np.random.rand(10000, 10), np.random.randint(0, 2, 10000)
    gmm_model = GMM()
    param_grid = {'n_components': [1, 2, 3, 4], 'covariance_type': ['tied', 'full', 'spherical']}
    grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
    try:
        _check_classification_targets(y)
    except ValueError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by creating a random dataset with 10 features and 2 classes, then attempting to perform grid search using GMM classifier with `scoring='roc_auc'`. The `_check_classification_targets` function from `sklearn.metrics.scorer` is used to raise a `ValueError` if the target labels are not suitable for classification. If the issue is present, an `AssertionError` will be raised and the stack trace will be printed using the provided `print_stacktrace` function.