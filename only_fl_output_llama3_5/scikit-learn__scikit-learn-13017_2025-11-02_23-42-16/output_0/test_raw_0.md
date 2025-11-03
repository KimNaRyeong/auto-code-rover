Here is the reproducer script:

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

try:
    X = np.random.randn(2, 2)
    X_categories = np.array([[1], [2]])
    X = np.concatenate([X, X_categories], axis=1)

    ohe = OneHotEncoder(categories='auto')
    tf_1 = ColumnTransformer([('ohe', ohe, [-1])], remainder='passthrough')
    result_1 = tf_1.fit_transform(X)
    
    tf_2 = ColumnTransformer([('ohe', ohe, [2])], remainder='passthrough')
    result_2 = tf_2.fit_transform(X)

    if np.array_equal(result_1, result_2):
        print("Issue not present")
        exit(0)
    else:
        raise AssertionError("Issue present")

except Exception as e:
    print_stacktrace(e)
    exit(1)
```

This script will run the `ColumnTransformer` with both negative and positive indices and compare the results. If the results are different, it will raise an `AssertionError`. If the issue is fixed, it will print a message and exit with code 0.