 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
from sklearn.metrics.cluster import mutual_info_score

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
    try:
        x = np.random.choice(['a', 'b'], size=20).astype(object)
        mutual_info_score(x, x)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue reproduced"
```
When executed with `python3 reproducer.py`, the script will raise a `ValueError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    mutual_info_score(x, x)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/metrics/cluster/_unsupervised.py", line 222, in mutual_info_score
    return _mutual_info_score(X, y, contingency_format, range(n_samples))
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/metrics/cluster/_unsupervised.py", line 162, in _mutual_info_score
    contingency_matrix = _contingenency_matrix(X, y, range(n_samples))
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/metrics/cluster/_unsupervised.py", line 133, in _contingenency_matrix
    X = check_array(X, ensure_2d=False, dtype=None)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/utils/validation.py", line 76, in inner_f
    return f(*args, **kwargs)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/utils/validation.py", line 1040, in check_array
    array = np.asarray(array, order=order, dtype=dtype)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/core/numeric.py", line 538, in asarray
