 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from scipy import sparse
from sklearn.impute import SimpleImputer

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

X = np.array([[0,0,0],[0,0,0],[1,1,1]])
X = sparse.csc_matrix(X)
X[0] = 0    # explicit zeros in first row

imp = SimpleImputer(missing_values=0, strategy='mean')
result = imp.fit_transform(X)
expected_result = np.array([[1. , 1. , 1. ],
                            [1. , 1. , 1. ],
                            [1. , 1. , 1. ]])

assert np.allclose(result, expected_result), "The imputed result does not match the expected result."
print_stacktrace(AssertionError("The imputed result does not match the expected result."))
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` with the stack trace if the issue is present. If the issue is fixed, the script will exit with code 0.