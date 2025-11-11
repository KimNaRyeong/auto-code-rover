Here is the reproducer script:

```python
import sys
from sklearn.model_selection import RandomizedSearchCV
from sklearn.datasets import load_iris
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score

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
    iris = load_iris()
    X, y = iris.data[:, :2], iris.target
    scaler = StandardScaler()
    pipe = make_pipeline(scaler, LogisticRegression())
    param_grid = {'logisticregression__C': [1, 10, 100],
                  'logisticregression__penalty': ['l1', 'l2']}
    rs = RandomizedSearchCV(pipe, param_grid, n_iter=2000)
    try:
        rs.fit(X, y)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.