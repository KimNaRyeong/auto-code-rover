 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sklearn
import sklearn.pipeline
import sklearn.ensemble
import sklearn.decomposition
import sklearn.linear_model
import numpy as np

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    init = sklearn.pipeline.make_pipeline(sklearn.decomposition.PCA(), sklearn.linear_model.ElasticNet())
    model = sklearn.ensemble.GradientBoostingRegressor(init=init)
    x = np.random.rand(12, 3)
    y = np.random.rand(12)
    try:
        model.fit(x, y)
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with `python3 reproducer.py`, the script will print the stack trace of the issue.

To fix the issue, the code in `sklearn/ensemble/gradient_boosting.py` should be modified as follows:
```python
def fit(self, X, y=None, sample_weight=None, **fit_params):
    if y is not None:
        # update init's fit method to accept sample_weight
        self.init_.fit(X, y, **fit_params, sample_weight=sample_weight)
    else:
        # use init's fit method directly
        self.init_.fit(X, **fit_params)
    return self
```
After applying the fix, the script should exit with code 0 when executed with `python3 reproducer.py`.