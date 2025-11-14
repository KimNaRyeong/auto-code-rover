Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

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
    X = np.random.randn(2, 2)
    X_categories = np.array([[1], [2]])
    X = np.concatenate([X, X_categories], axis=1)

    ohe = OneHotEncoder(categories='auto')
    tf_1 = ColumnTransformer([('ohe', ohe, [-1])], remainder='passthrough')
    try:
        tf_1.fit_transform(X)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected error"

    tf_2 = ColumnTransformer([('ohe', ohe, [2])], remainder='passthrough')
    tf_2.fit_transform(X)

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by attempting to use a negative index with `ColumnTransformer`. If the issue is present, it will raise an error and print the stack trace.