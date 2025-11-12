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
    
    param_grid = {'logistic_regression__C': [0.1, 1, 10], 
                  'logistic_regression__penalty': ['l1', 'l2']}
    model = LogisticRegression()
    random_search = RandomizedSearchCV(model, param_grid, n_iter=10000)
    
    try:
        random_search.fit(X_scaled, y)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a simple RandomizedSearchCV instance with a large number of iterations (10,000) and tries to fit it to the Iris dataset. Since the size of the search space is much smaller than 10,000, this should raise an exception when run. The `print_stacktrace` function will print the stack trace of the exception.