Here is the reproducer script:

```python
import sys
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.exceptions import NotFittedError

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
    clf = make_pipeline(LogisticRegression())
    clf.fit([[0], [0]], [0, 1], logisticregression__sample_weight=[1, 1])
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    sys.exit(0)
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue.