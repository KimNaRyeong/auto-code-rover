 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.datasets import fetch_openml
from sklearn.linear_model import Ridge
import sys

def print_stacktrace(e: Exception):
    import traceback   
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    census = fetch_openml(data_id=534, as_frame=True)
    X, y = census.data, census.target
    numerical_cols = ['AGE', 'EDUCATION', 'EXPERIENCE']
    model = Ridge(solver='sag').fit(X[numerical_cols], y)
except Exception as e:
    print_stacktrace(e)
    sys.exit(0)

# The following line should not be reached if the issue is present
assert False
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 16, in <module>
    model = Ridge(solver='sag').fit(X[numerical_cols], y)
  File "/Users/username/miniconda3/envs/scikit-learn-dev/lib/python3.8/site-packages/sklearn/linear_model/_base.py", line 94, in fit
    dataset = ArrayData(X, y, sample_weight, seed=seed)
  File "/Users/username/miniconda3/envs/scikit-learn-dev/lib/python3.8/site-packages/sklearn/utils/seq_dataset.pyx", line 126, in sklearn.utils.seq_dataset.ArrayDataset64.__cinit__
ValueError: ndarray is not C-contiguous
```
This stack trace shows that the issue is caused by a `ValueError` raised in the `ArrayDataset64.__cinit__` method, which is called by the `fit` method of the `Ridge` model. The error message indicates that the `X` array is not C-contiguous, which is a requirement for the `ArrayDataset64` constructor.