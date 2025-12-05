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

if __name__ == "__main__":
    X, y = datasets.make_classification(n_samples=10000, n_features=10, n_classes=2)
    gmm_model = GMM()
    param_grid = {'n_components': [1, 2, 3, 4],
                  'covariance_type': ['tied', 'full', 'spherical']}
    grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
    try:
        grid_search.fit(X, y)
    except Exception as e:
        print_stacktrace(e)
        raise e
```
When running the script, it should print the following stack trace:
```ruby
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    grid_search.fit(X, y)
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/model_selection/_search.py", line 721, in fit
    self._run_search(evaluate_candidates)
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/model_selection/_search.py", line 1149, in _run_search
    evaluate_candidates(ParameterGrid(self.param_grid))
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/model_selection/_search.py", line 712, in evaluate_candidates
    cv.split(X, y, groups))
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/externals/joblib/parallel.py", line 917, in __call__
    if self.dispatch_one_batch(iterator):
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/externals/joblib/parallel.py", line 731, in dispatch_one_batch
    self._dispatch(tasks)
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/externals/joblib/parallel.py", line 689, in _dispatch
    job = self._backend.apply_async(batch, callback=cb)
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/externals/joblib/_parallel_backends.py", line 182, in apply_async
    result = ImmediateResult(func)
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-packages/sklearn/externals/joblib/_parallel_backends.py", line 549, in __init__
    self.results = batch()
  File "/Users/user/miniconda3/envs/sklearn/lib/python3.8/site-