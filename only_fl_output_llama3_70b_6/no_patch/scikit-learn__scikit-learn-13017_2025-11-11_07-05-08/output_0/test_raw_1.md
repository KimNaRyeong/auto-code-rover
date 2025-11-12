Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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

def main():
    X = np.random.randn(2, 2)
    X_categories = np.array([[1], [2]])
    X = np.concatenate([X, X_categories], axis=1)

    ohe = OneHotEncoder(categories='auto')
    tf_1 = ColumnTransformer([('ohe', ohe, [-1])], remainder='passthrough')
    result_1 = tf_1.fit_transform(X)

    tf_2 = ColumnTransformer([('ohe', ohe, [2])], remainder='passthrough')
    result_2 = tf_2.fit_transform(X)

    try:
        if not np.array_equal(result_1, result_2):
            raise AssertionError("ColumnTransformer behavior for negative column indexes is not clear")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
<|start_header_id|>