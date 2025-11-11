The issue is not with the code you provided, but rather with the installation of scikit-learn. The error message suggests that scikit-learn has not been built correctly.

To reproduce this issue, we can create a simple script that tries to import scikit-learn:

```python
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

try:
    from sklearn import datasets
except Exception as e:
    print_stacktrace(e)
    sys.exit(1)

print("Issue reproduced successfully.")
sys.exit(0)
```

This script will raise an `AssertionError` if the issue is present, and it will print a stack trace of the issue. If the issue is fixed, it will exit with code 0.

Please note that this script does not reproduce the specific error you mentioned (`Zero division error in HistGradientBoosting`), but rather reproduces the installation issue you are experiencing.