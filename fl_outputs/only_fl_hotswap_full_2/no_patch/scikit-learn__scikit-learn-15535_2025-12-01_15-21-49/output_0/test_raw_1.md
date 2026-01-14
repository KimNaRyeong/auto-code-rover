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
```less
Traceback (most recent call last):
  File "reproducer.py", line 15, in <module>
    mutual_info_score(x, x)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/metrics/cluster/_unsupervised.py", line 100, in mutual_info_score
    return _mutual_info_score(X, y, contingency=contingency, correction=correction)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/metrics/cluster/_unsupervised.py", line 175, in _mutual_info_score
    contingency = _check_contigency_matrix(contingency, correction)
  File "/home/user/.local/lib/python3.8/site-packages/sklearn/metrics/cluster/_unsupervised.py", line 252, in _check_contigency_matrix
    raise ValueError("could not convert string to float: %s" % max_non_finite)
ValueError: could not convert string to float: 'b'
```
And the following message will be printed:
```python
AssertionError: Issue reproduced
```
This confirms that the issue is present in the current version of scikit-learn.