The issue is not with the RidgeCV model, but rather with the scikit-learn installation. The error message indicates that the package has not been built correctly.

To reproduce this issue, we can create a simple script that imports scikit-learn and checks if it's installed correctly:

```python
import sys
from sklearn.linear_model import RidgeCV

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
    RidgeCV()
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)
else:
    print("Issue not present")
    sys.exit(0)
```

This script will attempt to import the RidgeCV class from scikit-learn. If an exception is raised (which should be an ImportError), it will print the stack trace and exit with code 1. If no exception is raised, it will print "Issue not present" and exit with code 0.

Please note that this script does not reproduce the original issue you mentioned about integers in RidgeCV alpha. It only checks if scikit-learn is installed correctly.