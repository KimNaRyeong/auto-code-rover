Here is the reproducer script:

```python
import sklearn.datasets
import sklearn.model_selection
import sklearn.ensemble
from sklearn.base import BaseSearchCV
import time
import sys
import traceback

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
    X, y = sklearn.datasets.load_iris(return_X_y=True)

    rs = BaseSearchCV(
        estimator=sklearn.ensemble.RandomForestClassifier(),
        param_grid={'n_estimators': [2, 3, 4, 5]}
    )
    start_time = time.time()
    rs.fit(X, y)
    end_time = time.time()

    if not hasattr(rs, 'best_estimator_'):
        raise AssertionError("Best estimator is not available")
    best_estimator = rs.best_estimator_
    refit_start_time = time.time()
    best_estimator.fit(X, y)
    refit_end_time = time.time()

    if not hasattr(best_estimator, 'refit_time_'):
        print_stacktrace(AssertionError("Refit time is not available"))
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by trying to refit the best model after hyperparameter optimization. It checks if the `best_estimator_` attribute exists and then tries to fit it again. If the `refit_time_` attribute is not available, an `AssertionError` is raised with a stack trace printed.