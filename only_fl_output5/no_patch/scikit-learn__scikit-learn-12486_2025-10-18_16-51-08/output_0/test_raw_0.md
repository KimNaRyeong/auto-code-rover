```python
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

def test_gmm_grid_search():
    from sklearn import datasets
    from sklearn.model_selection import GridSearchCV
    from sklearn.mixture import GaussianMixture
    X, y = datasets.make_classification(n_samples=10000, n_features=10, n_classes=2)
    # Updated GMM model for newer sklearn versions
    gmm_model = GaussianMixture()
    # Standard param grid
    param_grid = {'n_components': [1, 2, 3, 4], 'covariance_type': ['tied', 'full', 'spherical']}
    try:
        grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
        grid_search.fit(X, y)
    except IndexError as e:
        print_stacktrace(e)
        raise AssertionError("IndexError occurred as expected due to the issue.") from e

if __name__ == '__main__':
    try:
        test_gmm_grid_search()
    except AssertionError as e:
        print("Error verified:", e)
    else:
        print("No error detected, the issue might have been resolved.")
```

This script will attempt to perform grid search using `GaussianMixture` (the updated name for `GMM` in newer versions of `sklearn`) with `roc_auc` scoring. The script uses an assertion to verify the presence of the `IndexError` that happens because `GaussianMixture` does not have a `predict_proba` method by default, which is required for `roc_auc` scoring on binary classification tasks. When the issue is present, the script prints a detailed stack trace. When the issue has been resolved, it exits with code 0, indicating successful execution without errors.