import numpy as np
from scipy import sparse
from sklearn.impute import SimpleImputer
import sys
import traceback

def print_stacktrace(e: Exception):
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

if not np.allclose(result, expected_result):
    raise AssertionError("The imputed result is not as expected.")
print_stacktrace(Exception("The imputed result is not as expected."))
