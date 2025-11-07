Here is a standalone Python file, designed in compliance with your specifications, to reproduce the reported issue. This script checks for the problematic behavior described in the initial problem statement and prints a clear stack trace upon encountering the `IndexError` to ease diagnostic processes. The error handling mechanism is rigorously defined to help identify whether the described bug exists, ensuring that the script exits with code 0 when the issue is resolved, as instructed.

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
    from sklearn import datasets
    from sklearn.model_selection import GridSearchCV
    # Import GaussianMixture for replacing deprecated GMM
    from sklearn.mixture import GaussianMixture as GMM

    X, y = datasets.make_classification(n_samples=100, n_features=10, n_classes=2)

    gmm_model = GMM()

    param_grid = {
        'n_components': [1, 2],
        'covariance_type': ['tied', 'full']
    }

    try:
        grid_search = GridSearchCV(gmm_model, param_grid, scoring='roc_auc')
        grid_search.fit(X, y)

    except IndexError as e:
        print_stacktrace(e)
        raise AssertionError("An IndexError occurred indicating the issue is present")

    print("No issue encountered - IndexError not raised by the script.")

if __name__ == '__main__':
    try:
        main()
    except AssertionError as error:
        print(error)
        exit(1)  # Exits with status 1 to indicate failure due to the issue being present
    exit(0)  # Exits with status 0 to indicate success - the issue is resolved
```

This script endeavors to target the specific problem involving the `GridSearchCV` with `GMM` model and `roc_auc` scoring. It encapsulates the logic inside the `main()` function and employs the previously defined `print_stacktrace` function for error reporting. This structure ensures the script can be executed as described, directly from the root directory of the project, and is expected to meet the requirements for diagnosing the mentioned issue.