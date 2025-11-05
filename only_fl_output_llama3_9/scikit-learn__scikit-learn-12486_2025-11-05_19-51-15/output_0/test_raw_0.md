Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from sklearn import datasets
from sklearn.grid_search import GridSearchCV
from sklearn.mixture import GMM
from sklearn.metrics import roc_auc_score

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
    X, y = datasets.make_classification(n_samples=10000, n_features=10, n_classes=2)
    gmm_model = GMM()
    param_grid = {'n_components': [1, 2, 3, 4], 'covariance_type': ['tied', 'full', 'spherical']}
    grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
    try:
        grid_search.fit(X, y)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by performing a GridSearchCV with a GMM classifier and scoring='roc_auc' on a classification problem. It then prints the stack trace of the exception that is raised when the issue occurs, and raises an AssertionError to indicate that the issue has been reproduced.

To run this script, simply execute it using Python: `python3 reproducer.py`. If the issue is present, you should see the stack trace printed to the console.