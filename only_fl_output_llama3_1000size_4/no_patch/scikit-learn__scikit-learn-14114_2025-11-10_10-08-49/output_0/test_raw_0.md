Here is the reproducer script:

```python
import numpy as np
from sklearn.ensemble import AdaBoostClassifier
from sklearn.svm import SVC
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
    X_train, X_test, y_train, y_test = train_test_split(iris.data, iris.target, test_size=0.5, random_state=42)

    try:
        AdaBoostClassifier(algorithm="SAMME", base_estimator=SVC()).fit(X_train, y_train).predict_proba(X_test)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script reproduces the issue by creating an AdaBoostClassifier with SAMME algorithm and SVC base estimator. It then tries to predict probabilities on test data, which should raise a `NotImplementedError` due to the incorrect usage of `predict_proba`. The script prints the stack trace and raises an `AssertionError` if the issue is not fixed.