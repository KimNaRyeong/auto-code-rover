Here is the reproducer script:

```python
import mlxtend.classifier as mc
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

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
    iris = load_iris()
    X, y = iris.data, iris.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.5, random_state=42)

    # Train base estimators
    base_estimators = [RandomForestClassifier(n_estimators=10, random_state=42) for _ in range(3)]
    for estimator in base_estimators:
        estimator.fit(X_train, y_train)

    # Try to train final estimator with original dataset when it should not be used
    try:
        mc.StackingCVClassifier(estimators=base_estimators, use_features_in_secondary=True)
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == '__main__':
    reproduce_issue()
```

This script will attempt to create a `StackingCVClassifier` with the option `use_features_in_secondary=True`, which should raise an `AssertionError`. The script will then print the stack trace of the error and exit with code 0.