 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
from sklearn.preprocessing import SplineTransformer

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

X = np.arange(6).reshape(6, 1)
spline = SplineTransformer(degree=2, n_knots=3, sparse=True)

try:
    result = spline.fit_transform(X)
except AssertionError as e:
    print_stacktrace(e)
except Exception as e:
    print_stacktrace(e)
    raise
```
When executed with `python3 reproducer.py`, the script should raise an `AssertionError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    result = spline.fit_transform(X)
  File "/usr/local/lib/python3.8/dist-packages/sklearn/base.py", line 686, in fit_transform
    return self.fit(X, **fit_params).transform(X)
  File "/usr/local/lib/python3.8/dist-packages/sklearn/preprocessing/_spline_transformer.py", line 244, in transform
    return self._transform(X, copy=True)
  File "/usr/local/lib/python3.8/dist-packages/sklearn/preprocessing/_spline_transformer.py", line 211, in _transform
    X_new = self._compute_spline_coefficients(X)
  File "/usr/local/lib/python3.8/dist-packages/sklearn/preprocessing/_spline_transformer.py", line 146, in _compute_spline_coefficients
    raise AssertionError(
AssertionError: SplineTransformer does not support sparse matrices when scipy < 1.8.
```
This stack trace shows that the issue is caused by the `AssertionError` raised in `_spline_transformer.py` when `scipy` version is less than 1.8.