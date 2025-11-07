Given the instructions and ensuring compatibility with Python 3 and the latest practices, here's a revised version of the `reproducer.py` script:

```python
# reproducer.py
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

def main():
    try:
        from sklearn import datasets
        from sklearn.model_selection import GridSearchCV
        from sklearn.mixture import GaussianMixture as GMM
        import sys

        # Note: Changing the import from sklearn.grid_search to sklearn.model_selection
        # and using GaussianMixture instead of GMM from sklearn.mixture for compatibility with newer sklearn versions

        X, y = datasets.make_classification(n_samples=1000, n_features=10, n_classes=2)

        gmm_model = GMM()

        param_grid = {
            'n_components': [1, 2, 3, 4],
            'covariance_type': ['tied', 'full', 'spherical']
        }

        grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
        grid_search.fit(X, y)

        assert False, "The issue did not occur."
    except AssertionError as e:
        print_stacktrace(e)
    except Exception as e:
        print_stacktrace(e)
        raise
    else:
        print("No AssertionError encountered. The issue might have been fixed.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by fitting a `GaussianMixture` model using `GridSearchCV` with `roc_auc` scoring. The `AssertionError` is raised if none of the expected exceptions occur, ideally identifying if the problem exists. If an exception related to the original issue is caught, it prints the detailed stack trace. This approach ensures that the script can be executed in an environment with a properly installed Scikit-learn library.