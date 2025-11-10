Based on the provided information, it seems that the issue is not with the `RidgeClassifierCV` class itself but rather with the installation of scikit-learn. The error message indicates that scikit-learn has not been built correctly.

Here's a standalone Python file `reproducer.py` to reproduce the issue:

```python
import sys
import traceback

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
    from sklearn import linear_model as lm
except ImportError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
```

This script attempts to import the `linear_model` module from scikit-learn. If this raises an `ImportError`, it prints the stack trace and exits with code 1. If no error is raised, it exits with code 0.

To run this script, save it in a file named `reproducer.py` and execute it using Python: `python3 reproducer.py`.