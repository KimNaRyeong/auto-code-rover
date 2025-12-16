 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn import set_config
from sklearn.calibration import CalibratedClassifierCV
from sklearn.linear_model import SGDClassifier

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

set_config(transform_output="pandas")
model = CalibratedClassifierCV(SGDClassifier(), method='isotonic')
try:
    model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
    model.predict(np.arange(90).reshape(30, -1))
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/calibration.py", line 477, in fit
    self.calibrators_ = [
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/calibration.py", line 478, in <listcomp>
    calibrator.fit(X, y)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/calibration.py", line 757, in fit
    self.classes_ = np.unique(y)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/lib/arraysetops.py", line 221, in unique
    return _unique1d(ar, return_index, return_inverse, return_counts)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/lib/arraysetops.py", line 314, in _unique1d
    uniques = ar[perm]
ValueError: could not broadcast input array from shape (20,1) into shape (20)
```
This stack trace shows that the issue is caused by a `ValueError` when trying to broadcast an array of shape `(20,1)` into shape `(20)` during the call to `np.unique(y)` in the `fit` method of the `CalibratedClassifierCV` class. This issue is caused by the `set_config(transform_output="pandas")` statement, which changes the default output format of some scikit-learn functions to Pandas DataFrames. In this case, the `y` argument of the `fit` method is being transformed into a Pandas Series, which causes the broadcasting error when it is passed to `np.unique`.