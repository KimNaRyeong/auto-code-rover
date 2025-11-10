Here is the reproducer script:

```python
import numpy as np
from sklearn.preprocessing import OneHotEncoder
import sklearn
import sys
import traceback

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    enc = OneHotEncoder(dtype=np.float32, categorical_features=[0, 1])
    x = np.array([[0, 1, 0, 0], [1, 2, 0, 0]], dtype=int)
    sparse = enc.fit(x).transform(x)
    expected_dtype = np.dtype(np.float32)
    actual_dtype = sparse.format.asformat().dtype
    assert actual_dtype == expected_dtype, "OneHotEncoder does not output scipy sparse matrix of given dtype"
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
```