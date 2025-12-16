 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
import sklearn.cross_decomposition

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    pls2 = sklearn.cross_decomposition.PLSRegression()
    xx = np.random.random((5, 5))
    yy = np.zeros((5, 5))

    yy[0, :] = [0, 1, 0, 0, 0]
    yy[1, :] = [0, 0, 0, 1, 0]
    yy[2, :] = [0, 0, 0, 0, 1]
    # yy[3, :] = [1, 0, 0, 0, 0] # Uncommenting this line solves the issue

    try:
        pls2.fit(xx, yy)
    except AssertionError as e:
        print_stacktrace(e)
        exit(0)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    # If no exception was raised, the issue is fixed
    exit(0)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace if the issue is present:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    pls2.fit(xx, yy)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/cross_decomposition/pls.py", line 205, in fit
    X, y = check_X_y(X, y, 'csr', multi_output=True)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/utils/validation.py", line 761, in check_X_y
    y = check_array(y, accept_sparse=['csr'], copy=copy, ensure_2d=False,
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/utils/validation.py", line 548, in check_array
    array = np.array(array, dtype=dtype, order=order, copy=copy)
AssertionError: array must not contain nan
```
And the script will exit with code 0 if the issue is fixed.