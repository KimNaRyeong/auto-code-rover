Here is the reproducer script:

```python
import numpy as np
from scipy import sparse
from sklearn.impute import SimpleImputer
import traceback
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    X = np.array([[0,0,0],[0,0,0],[1,1,1]])
    X = sparse.csc_matrix(X)
    X[0] = 0
    imp = SimpleImputer(missing_values=0, strategy='mean')
    result = imp.fit_transform(X)

    if not np.array_equal(result, [[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]]) :
        raise AssertionError("Expected result does not match")

except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed")
exit(0)
```

This script will run the test and if it fails, it will print the stack trace of the failure. If the test passes, it will print "Test passed" and exit with code 0.