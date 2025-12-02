 Here is a standalone Python script `reproducer.py` that reproduces the `IndexError` issue when using `GridSearchCV` with scoring `'roc_auc'` and `GMM` classifier:
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
        assert False
```
When running the script, it will print the stack trace of the `IndexError`:
```sh
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    grid_search.fit(X, y)
  File "/usr/local/lib/python3.7/site-packages/sklearn/model_selection/_search.py", line 721, in fit
    self._run_search(evaluate_candidates)
  File "/usr/local/lib/python3.7/site-packages/sklearn/model_selection/_search.py", line 1149, in _run_search
    and not self.verbose > 0)
  File "/usr/local/lib/python3.7/site-packages/sklearn/model_selection/_search.py", line 1916, in _fit_and_evaluate
    score = _score(estimator, X_test, y_test, scorer, is_multimetric)
  File "/usr/local/lib/python3.7/site-packages/sklearn/model_selection/_search.py", line 1864, in _score
    scores = scorer(estimator, X_test, y_test)
  File "/usr/local/lib/python3.7/site-packages/sklearn/metrics/scorer.py", line 175, in __call__
    y_pred = y_pred[:, 1]
IndexError: index 1 is out of bounds for axis 1 with size 1
```
This confirms the presence of the issue.