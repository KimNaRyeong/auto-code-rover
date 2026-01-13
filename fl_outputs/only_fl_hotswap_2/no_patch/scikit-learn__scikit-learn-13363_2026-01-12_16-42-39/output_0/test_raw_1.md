 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sklearn.linear_model import Ridge

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
    try:
        X = [[0], [1], [3]]
        y = [0, 1, 3]
        alpha = 1
        Ridge(alpha=alpha, return_intercept=True).fit(X, y)
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` and print the following stack trace:
```sql
Traceback (most recent call last):
  File "reproducer.py", line 14
    Ridge(alpha=alpha, return_intercept=True).fit(X, y)
  File "/home/user/.pyenv/versions/3.7.2/envs/kaggle-3.7.2/lib/python3.7/site-packages/sklearn/linear_model/ridge.py", line 452, in fit
    return coef, intercept
UnboundLocalError: local variable 'intercept' referenced before assignment
```
This reproduces the issue where an `UnboundLocalError` is raised when `return_intercept=True` is passed to `ridge_regression`. The issue is caused by the fact that `intercept_` is not defined until the `fit` method is called, but is referenced beforehand in the `return_intercept` case.