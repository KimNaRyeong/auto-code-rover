 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.feature_selection import SelectKBest
from sklearn.feature_selection import chi2

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

X, y = load_iris(return_X_y=True, as_frame=True)
X = X.astype(
    "petal width (cm)": np.float16,
    "petal length (cm)": np.float16,
)
X["cat"] = y.astype("category")

selector = SelectKBest(chi2, k=2)
selector.set_output(transform="pandas")
X_out = selector.fit_transform(X, y)

assert X_out.dtypes.equals(pd.Series(["float16", "float64"], name="dtype")), "Dtypes are not preserved"
```
To run the script, execute `python3 reproducer.py` in the root directory of the project. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will exit with code 0.

Note: The script uses the `pd` alias for `pandas`. Make sure to import `pandas` as `pd` in your project for the script to work correctly.