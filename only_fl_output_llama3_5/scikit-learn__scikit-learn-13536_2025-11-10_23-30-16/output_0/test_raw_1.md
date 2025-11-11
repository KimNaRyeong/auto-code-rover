The issue seems to be related to the installation of scikit-learn. The error message suggests that the package has not been built correctly.

To reproduce this issue, you can try installing scikit-learn from source and then running the reproducer script. Here is a standalone python file `reproducer.py`:

```
import sklearn.pipeline as pipeline
from sklearn.linear_model import LogisticRegression

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
    try:
        from sklearn.pipeline import make_pipeline
        clf = pipeline.make_pipeline(LogisticRegression())
        clf.fit([[0], [0]], [0, 1], sample_weight=[1, 1])
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

This script will attempt to create a pipeline with LogisticRegression and then try to fit it using sample weights. If the issue is present, it will print the stack trace and raise an `AssertionError`.