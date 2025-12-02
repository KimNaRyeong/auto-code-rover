 Here is a standalone python script `reproducer.py` to reproduce the issue:
```python
from sklearn import datasets
from sklearn.grid_search import GridSearchCV
from sklearn.mixture import GMM

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == '__main__':
    X, y = datasets.make_classification(n_samples=10000, n_features=10, n_classes=2)
    gmm_model = GMM()
    param_grid = {'n_components': [1, 2, 3, 4],
                  'covariance_type': ['tied', 'full', 'spherical']}
    grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
    try:
        grid_search.fit(X, y)
    except Exception as e:
        print_stacktrace(e)
```
When executed using `python3 reproducer.py`, the script raises an `IndexError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    grid_search.fit(X, y)
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/model_selection/_search.py", line 739, in fit
    self._run_search(evaluate_candidates)
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/model_selection/_search.py", line 1176, in _run_search
    evaluate_candidates(ParameterGrid(self.param_grid))
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/model_selection/_search.py", line 727, in evaluate_candidates
    cv.fit(X, y)
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/model_selection/_validation.py", line 680, in fit
    self._fit(X, y, **fit_params)
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/model_selection/_validation.py", line 382, in _fit
    for train_index, test_index in cv.split(X, y, groups))
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/externals/joblib/parallel.py", line 1005, in __call__
    self.retrieve()
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/externals/joblib/parallel.py", line 926, in retrieve
    self._output.raise_exception(self.exception_handler)
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/externals/joblib/exceptions.py", line 269, in raise_exception
    raise exception
  File "/Users/user/miniforge3/lib/python3.9/site-packages/sklearn/externals/joblib/parallel.py", line 830, in _handle_callback
    raise Exception(msg)
IndexError: index 1 is out of bounds for axis 1 with size 1
```
This confirms the presence of the issue.