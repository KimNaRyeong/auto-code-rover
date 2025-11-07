Here is the reproducer script:

```python
import sys
from sklearn.linear_model import RidgeCV
from sklearn.datasets import make_regression

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

try:
    X, y = make_regression()
    ridge = RidgeCV(alphas=[1, 10, 100, 1000]).fit(X, y)
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue not present")
    sys.exit(0)
```

This script will attempt to reproduce the issue by creating a RidgeCV model with integer alphas. If an exception is raised (which should be a ValueError), it will print the stack trace and exit with code 1. If no exception is raised, it will print "Issue not present" and exit with code 0.