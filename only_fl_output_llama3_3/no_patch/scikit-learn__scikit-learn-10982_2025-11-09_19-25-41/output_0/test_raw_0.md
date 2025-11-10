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
    cv = RandomizedSearchCV(model, param_grid, n_iter=10000)
    
    try:
        cv.fit(X_scaled, y)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a random search for logistic regression with a grid of 3x2 and tries to run it with `n_iter=10000`, which is greater than the size of the grid. This should raise an exception, which will be caught and printed by the `print_stacktrace` function.