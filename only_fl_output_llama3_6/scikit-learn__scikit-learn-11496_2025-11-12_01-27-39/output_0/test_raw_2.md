Here is the reproducer script:

```python
import numpy as np
from scipy import sparse
from sklearn.impute import SimpleImputer
from sklearn.utils.testing import assert_raises
import traceback
import sys

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

def reproducer():
    X = np.array([[0,0,0],[0,0,0],[1,1,1]])
    X = sparse.csc_matrix(X)
    X[0] = 0
    imp = SimpleImputer(missing_values=0, strategy='mean')
    try:
        result = imp.fit_transform(sparse.csr_matrix(X))
        assert result.all() == np.array([[1., 1., 1.]]), "Expected all values to be 1."
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproducer()
```

This script will run the reproducing code and raise an `AssertionError` when the issue is present. The stack trace of the issue will be printed to the console.