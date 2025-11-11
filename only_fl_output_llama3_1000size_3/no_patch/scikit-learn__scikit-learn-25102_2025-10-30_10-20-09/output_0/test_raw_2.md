Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.preprocessing import StandardScaler
import pandas as pd

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

def reproduce_issue():
    X, y = load_iris(return_X_y=True, as_frame=True)
    X = X.astype({
        "petal width (cm)": np.float16,
        "petal length (cm)": np.float16,
    })
    X["cat"] = y.astype("category")

    selector = SelectKBest(chi2, k=2)
    selector.set_output(transform="pandas")
    X_out = selector.fit_transform(X)

    if not pd.api.types.is_dtype_equal(X.dtypes, X_out.dtypes):
        raise AssertionError("dtypes are not preserved")

try:
    reproduce_issue()
except Exception as e:
    print_stacktrace(e)
finally:
    import sys
    sys.exit(0 if "AssertionError" not in str(e) else 1)
```

This script creates a DataFrame with categorical data, applies the `SelectKBest` transformer to select features, and checks whether the dtypes are preserved. If the dtypes are not preserved, it raises an `AssertionError`.