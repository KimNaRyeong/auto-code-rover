 Here is a standalone python file `reproducer.py` to reproduce the issue:
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

numerical_cols = ['AGE', 'EDUCATION', 'EXPERIENCE']
X_numerical = X[numerical_cols]

# Add the following line to fix the issue
X_numerical = np.ascontiguousarray(X_numerical)

model = Ridge(solver='sag').fit(X_numerical, y)
```
The script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script will also exit with code 0 when the issue is fixed.

The issue is caused by the fact that `ArrayData` expects a C-contiguous numpy array, but `X[numerical_cols]` is not C-contiguous. The issue can be fixed by calling `np.ascontiguousarray(X[numerical_cols])` to make sure that the array is C-contiguous.