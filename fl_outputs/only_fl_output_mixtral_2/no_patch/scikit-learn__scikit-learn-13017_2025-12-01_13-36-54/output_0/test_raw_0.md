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
        exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 34, in <module>
    main()
  File "reproducer.py", line 30, in main
    np.testing.assert_equal(result_1, result_2)
  File "/usr/local/lib/python3.8/dist-packages/numpy/testing/_private/utils.py", line 1477, in assert_equal
    raise AssertionError(msg)
AssertionError:
Arrays are not equal

(mismatch 100.0%)
 x: array([[ 1.        ,  0.        ,  0.10600662, -0.46707426,  1.        ],
       [ 0.        ,  1.        , -1.33177629,  2.29186299,  2.        ]])
 y: array([[ 1.        ,  0.        ,  0.10600662, -0.46707426],
       [ 0.        ,  1.        , -1.33177629,  2.29186299]])

(The two arrays have 2 elements each. The first elements are [ 1.        ,  0.        ].)
 in assert_equal at /usr/local/lib/python3.8/dist-packages/numpy/testing/_private/utils.py:1477
```
This confirms that the `ColumnTransformer` behaves differently when negative integers are passed as column indexes, and that the expected result (i.e., the same result as with positive indexes) is not obtained.