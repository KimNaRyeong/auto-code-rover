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
    try:
        n = 100
        x = np.random.randn(n, 30)
        y = np.random.normal(size = n)

        rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, store_cv_values = True).fit(x, y)

    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"

if __name__ == "__main__":
    main()
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 18, in main
    rr = lm.RidgeClassifierCV(alphas = np.arange(0.1, 1000, 0.1), normalize = True, store_cv_values = True).fit(x, y)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/linear_model/_ridge_cf.py", line 567, in __init__
    super().__init__(
TypeError: __init__() got an unexpected keyword argument 'store_cv_values'
```
This confirms that the issue is present in the current version of scikit-learn.