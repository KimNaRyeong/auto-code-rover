Here is the reproducer script:

```python
import sklearn.datasets
import sklearn.model_selection
import sklearn.ensemble
from sklearn.metrics import accuracy_score
from time import time

X, y = sklearn.datasets.load_iris(return_X_y=True)

rs = sklearn.model_selection.GridSearchCV(
    estimator=sklearn.ensemble.RandomForestClassifier(),
    param_grid={'n_estimators': [2, 3, 4, 5]}
)
rs.fit(X, y)

best_model = rs.best_estimator_
start_time = time()
best_model.fit(X, y)
end_time = time()

refit_time = end_time - start_time

assert refit_time > 0.1, "Refit time is too small"

print_stacktrace(AssertionError("Refit time is too small"))
```

This script reproduces the issue by measuring the time it takes to refit the best model after hyperparameter optimization and asserting that this time is greater than a certain threshold (0.1 seconds). If the assertion fails, it prints the stack trace of the exception.