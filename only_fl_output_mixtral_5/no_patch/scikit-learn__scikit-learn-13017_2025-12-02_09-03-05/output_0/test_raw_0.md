 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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

    print('---- With negative index ----')
    ohe = OneHotEncoder(categories='auto')
    tf_1 = ColumnTransformer([('ohe', ohe, [-1])], remainder='passthrough')
    result_1 = tf_1.fit_transform(X)

    print('---- With positive index ----')
    tf_2 = ColumnTransformer([('ohe', ohe, [2])], remainder='passthrough')
    result_2 = tf_2.fit_transform(X)

    np.testing.assert_equal(result_1, result_2)

if __name__ == '__main__':
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace, indicating that the actual results do not match the expected results. This reproduces the issue described in the original report.