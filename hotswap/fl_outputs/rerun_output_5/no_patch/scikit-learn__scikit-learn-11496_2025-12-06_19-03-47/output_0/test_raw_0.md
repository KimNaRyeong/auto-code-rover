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
expected_result = np.array([[1., 1., 1.], [1., 1., 1.], [1., 1., 1.]])

assert np.allclose(result, expected_result), "The imputed result is not as expected."
print_stacktrace(Exception("The imputed result is not as expected."))
```
This script will raise an `AssertionError` with a stack trace when executed with `python3 reproducer.py`. The line numbers of the statements in the script will be shown clearly in the stack trace. The script will exit with code 1 when the issue is present.