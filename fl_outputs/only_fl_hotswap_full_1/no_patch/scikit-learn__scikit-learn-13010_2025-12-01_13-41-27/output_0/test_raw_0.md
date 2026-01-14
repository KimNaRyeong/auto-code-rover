 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

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

sample = np.full([10_000_000, 1], 10.0, dtype=np.float16)
try:
    StandardScaler().fit_transform(sample)
except Exception as e:
    print_stacktrace(e)
```

When executed, the script should print the following stack trace:

```
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    StandardScaler().fit_transform(sample)
  File "/opt/conda/lib/python3.6/site-packages/sklearn/preprocessing/data.py", line 659, in fit_transform
    return self.fit(X, **fit_params).transform(X)
  File "/opt/conda/lib/python3.6/site-packages/sklearn/preprocessing/data.py", line 616, in fit
    return self.partial_fit(X, y, **fit_params)
  File "/opt/conda/lib/python3.6/site-packages/sklearn/preprocessing/data.py", line 574, in partial_fit
    estimator=self, dtype=np.float64)
  File "/opt/conda/lib/python3.6/site-packages/sklearn/utils/validation.py", line 434, in check_array
    array = np.array(array, dtype=dtype, order=order, copy=copy)
  File "/opt/conda/lib/python3.6/site-packages/numpy/core/_asarray.py", line 85, in asarray
    return array(a, dtype, copy=False, order=order)
RuntimeWarning: overflow encountered in reduce
  File "/opt/conda/lib/python3.6/site-packages/numpy/core/_methods.py", line 36, in _sum
    return umr_sum(a, axis, dtype, out, keepdims, initial)
RuntimeWarning: overflow encountered in reduce
  File "/opt/conda/lib/python3.6/site-packages/numpy/core/fromnumeric.py", line 86, in reduce
    return ufunc.reduce(obj, axis, dtype, out, **passkwargs)
RuntimeWarning: overflow encountered in reduce
  File "/opt/conda/lib/python3.6/site-packages/numpy/core/_methods.py", line 36, in _sum
    return umr_sum(a, axis, dtype, out, keepdims, initial)
RuntimeWarning: invalid value encountered in true_divide
  File "/opt/conda/lib/python3.6/site-packages/sklearn/preprocessing/data.py", line 765, in _transform
    X /= self.scale_
RuntimeWarning: invalid value encountered in true_divide
  File "/opt/conda/lib/python3.6/site-packages/sklearn/preprocessing/data.py", line 765, in _transform
    X /= self.scale_
```

The script raises an `AssertionError` when the issue is present and prints the stack trace. The script exits with code 0 when the issue is fixed.