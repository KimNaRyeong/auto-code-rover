Here is the standalone Python file `reproducer.py` to reproduce the issue:

```py
import sklearn.pipeline as pipeline
from sklearn.linear_model import LogisticRegression
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
    X_train, X_test, y_train, _ = train_test_split(iris.data, iris.target, test_size=0.5, random_state=42)
    
    try:
        clf = pipeline.make_pipeline(LogisticRegression())
        clf.fit(X_train, y_train, logisticregression__sample_weight=[1]*len(y_train))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to create a pipeline with a LogisticRegression estimator and then fit it using sample weights. If the issue is present, an `AssertionError` will be raised and the stack trace printed.