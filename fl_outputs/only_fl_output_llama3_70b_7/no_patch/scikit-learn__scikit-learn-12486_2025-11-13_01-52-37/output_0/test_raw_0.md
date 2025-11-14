Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from sklearn import datasets
    from sklearn.model_selection import GridSearchCV
    from sklearn.mixture import GMM

    X, y = datasets.make_classification(n_samples=10000, n_features=10, n_classes=2)
    gmm_model = GMM()
    param_grid = {'n_components': [1, 2, 3, 4],
                  'covariance_type': ['tied', 'full', 'spherical']}
    grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
    grid_search.fit(X, y)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue is present")
```
This script will reproduce the issue and raise an `AssertionError` with a stack trace when the issue is present. If the issue is fixed, it will exit with code 0.