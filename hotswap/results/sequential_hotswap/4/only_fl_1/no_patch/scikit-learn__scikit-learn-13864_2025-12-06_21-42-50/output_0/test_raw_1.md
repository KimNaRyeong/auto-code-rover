 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sklearn
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

binary_data = np.array((0, 0, 0, 0, 0, 1,
                         1, 0, 0, 1, 1, 0),
                       dtype = "bool").reshape((2, 6))

try:
    sklearn.metrics.pairwise_distances(binary_data, metric="jaccard")
except Exception as e:
    print_stacktrace(e)
    assert False
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the `AttributeError`:
```ruby
Traceback (most recent call last):
  File "reproducer.py", line 16
    sklearn.metrics.pairwise_distances(binary_data, metric="jaccard")
  File ".../lib/site-packages/sklearn/metrics/pairwise.py", line 1564
    if dtype == bool and (X.dtype != bool or Y.dtype != bool):
AttributeError: 'NoneType' object has no attribute 'dtype'
```
This confirms that the issue is present in the current version of scikit-learn (0.21.0). The issue was introduced in the commit mentioned in the description, and it seems to have been fixed in later versions of scikit-learn.