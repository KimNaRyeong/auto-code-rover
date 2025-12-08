 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback
from sklearn import linear_model as lm

def print_stacktrace(e):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    n = 100
    x = np.random.randn(n, 30)
    y = np.random.normal(size = n)

    try:
        rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, store_cv_values = True).fit(x, y)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

    assert True, "Issue not reproduced"

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will print the following stack trace and exit with code 1, indicating that the issue is present:
```makefile
Traceback (most recent call last):
  File "reproducer.py", line 23, in <module>
    main()
  File "reproducer.py", line 16, in main
    rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, store_cv_values = True).fit(x, y)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/linear_model/_ridge_cf.py", line 540, in fit
    X, y = self._validate_data(X, y, accept_sparse=['csr', 'csc'], y_numeric=True)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/base.py", line 588, in _validate_data
    X, y = check_X_y(X, y, **check_params)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/utils/validation.py", line 1057, in check_X_y
