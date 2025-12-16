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
When executed with `python3 reproducer.py`, the script should raise a `ValueError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    model.fit(np.arange(90).reshape(30, -1), np.arange(30) % 2)
  File "/home/philippe/.anaconda3/envs/strategy-training/lib/python3.9/site-packages/sklearn/calibration.py", line 477, in fit
    self.calibrators_[i] = calibration_func(
  File "/home/philippe/.anaconda3/envs/strategy-training/lib/python3.9/site-packages/sklearn/calibration.py", line 764, in calibrate_isotonic
    proba[:, class_idx] = calibrator.predict(this_pred)
ValueError: could not broadcast input array from shape (20,1) into shape (20,)
```
This reproduces the issue where `CalibratedClassifierCV` with isotonic regression doesn't work when `set_config(transform_output="pandas")` is previously set. The IsotonicRegression seems to return a dataframe, which is a problem for `_CalibratedClassifier` in `predict_proba` where it tries to put the dataframe in a numpy array row `proba[:, class_idx] = calibrator.predict(this_pred)`.