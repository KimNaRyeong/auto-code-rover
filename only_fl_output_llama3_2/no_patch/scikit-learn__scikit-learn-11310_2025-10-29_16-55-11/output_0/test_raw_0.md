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
start_time = time()
rs.fit(X, y)
end_time = time()

print("Time to fit and score each model:", end_time - start_time)

try:
    rs.refit()
except AttributeError as e:
    print_stacktrace(e)
    assert False, "Expected 'refit' attribute"
```

This script will run the grid search, measure the total time it takes, then try to refit the best model. If the `refit` method is not available (which is the case in this version of scikit-learn), an `AttributeError` will be raised and caught by the script. The stack trace will be printed and the script will fail with an assertion error.