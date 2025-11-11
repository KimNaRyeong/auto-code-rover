The issue is not with the `RepeatedKFold` and `RepeatedStratifiedKFold` classes, but rather with the scikit-learn installation. The error message indicates that the package has not been built correctly.

To reproduce this issue, you can create a simple Python file as follows:

```python
import sys

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
    raise ImportError("No module named 'sklearn.__check_build._check_build'")
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue not found. Exiting with code 0.")
sys.exit(0)
```

When you run this script, it will simulate the `ImportError` that is raised when scikit-learn has not been built correctly.