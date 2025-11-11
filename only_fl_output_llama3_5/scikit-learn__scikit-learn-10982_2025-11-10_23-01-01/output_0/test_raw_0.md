Here is the reproducer script:

```python
import sys
from sklearn.model_selection import RandomizedSearchCV
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler

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
    X, y = load_iris(return_X_y=True)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    param_grid = {'logistic_regression__C': [1, 10], 'logistic_regression__penalty': ['l1', 'l2']}
    random_search = RandomizedSearchCV(LogisticRegression(), param_grid, n_iter=1000)

    try:
        random_search.fit(X_scaled, y)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.