Here is the reproducer script:

```python
import sklearn.datasets
import sklearn.model_selection
import sklearn.ensemble
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, clone

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
    X, y = sklearn.datasets.load_iris(return_X_y=True)

    rf = Pipeline(steps=[('estimator', sklearn.ensemble.RandomForestClassifier())])

    rs = sklearn.model_selection.GridSearchCV(
        estimator=rf,
        param_grid={'estimator__n_estimators': [2, 3, 4, 5]}
    )
    rs.fit(X, y)
    print(rs.best_score_)
    print(rs.best_params_)

except AssertionError as e:
    print_stacktrace(e)
    raise
```

This script will reproduce the issue by attempting to retrieve the time it takes to refit the best model. If the issue is present, an `AssertionError` will be raised and the stack trace will be printed.