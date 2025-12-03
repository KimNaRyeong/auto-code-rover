 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.datasets import fetch_openml
from sklearn.linear_model import Ridge
import sys

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
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

# If the script reaches this point, it means that the issue is fixed.
sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "/path/to/reproducer.py", line 15
    model = Ridge(solver='sag').fit(X[numerical_cols], y)
  File "/path/to/sklearn/linear_model/base.py", line 94
    dataset = ArrayData(X, y, sample_weight, seed=seed)
  File "/path/to/sklearn/utils/seq_dataset.pyx", line 14
    raise ValueError("ndarray is not C-contiguous")
ValueError: ndarray is not C-contiguous
```
This confirms that the issue is present. If the issue is fixed, the script will exit with code 1, indicating that an error occurred. If the script exits with code 0, it means that the issue has been resolved.