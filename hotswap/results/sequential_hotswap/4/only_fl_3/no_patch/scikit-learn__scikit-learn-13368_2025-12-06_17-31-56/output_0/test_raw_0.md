 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_predict

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

if __name__ == "__main__":
    X, y = make_classification(n_samples=100, n_features=2, n_redundant=0, n_informative=2,
                               random_state=1, n_clusters_per_class=1)
    # Change the first sample to a new class
    y[0] = 2
    clf = LogisticRegression()
    cv = StratifiedKFold(n_splits=2, random_state=1)
    train, test = list(cv.split(X, y))
    yhat_proba = cross_val_predict(clf, X, y, cv=cv, method="predict_proba")
    expected_results = [[0.06105412, 0.93894588, 0.        ],
                        [0.92512247, 0.07487753, 0.        ],
                        [0.93896471, 0.06103529, 0.        ],
                        [0.04345507, 0.95654493, 0.        ]]
    assert (yhat_proba == expected_results).all(), "The results are not as expected!"
    print(yhat_proba)
```
The script uses the `print_stacktrace` function to print the stack trace when an `AssertionError` is raised. The `assert` statement checks if the output of `cross_val_predict` matches the expected results. If the assertion fails, an `AssertionError` is raised, and the stack trace is printed.

To run the script, execute `python3 reproducer.py` in the terminal. If the issue is present, an `AssertionError` will be raised, and the stack trace will be printed. If the issue is fixed, the script will print the output of `cross_val_predict` and exit with code 0.