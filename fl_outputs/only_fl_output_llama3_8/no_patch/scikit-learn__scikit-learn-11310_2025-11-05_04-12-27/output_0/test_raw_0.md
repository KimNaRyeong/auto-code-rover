Here is the reproducer script:

```python
import sklearn.datasets
import sklearn.model_selection
import sklearn.ensemble
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from timeit import default_timer as timer

X, y = sklearn.datasets.load_iris(return_X_y=True)

estimator = Pipeline([
    ('scaler', StandardScaler()),
    ('rfc', sklearn.ensemble.RandomForestClassifier())
])

param_grid = {'rfc__n_estimators': [2, 3, 4, 5]}

rs = sklearn.model_selection.GridSearchCV(
    estimator=estimator,
    param_grid=param_grid,
    cv=5
)

start_time = timer()
rs.fit(X, y)
end_time = timer()

refit_time = end_time - start_time

try:
    assert 'refit_time_' in rs.cv_results_
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print(f"Refitting the best model took {refit_time} seconds.")
```

This script reproduces the issue by attempting to access the `refit_time_` attribute, which does not exist. The `print_stacktrace` function is used to print the stack trace of the `AssertionError`.