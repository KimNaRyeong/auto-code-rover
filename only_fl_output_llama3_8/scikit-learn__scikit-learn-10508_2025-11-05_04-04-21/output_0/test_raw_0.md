Here is the reproducer script:

```python
import numpy as np
from sklearn.preprocessing import LabelEncoder
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

def reproduce_issue():
    le = LabelEncoder()
    le.fit([1,2])
    try:
        le.transform([])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        reproduce_issue()
        sys.exit(0)  # exit with code 0 if the issue is fixed
    except AssertionError:
        sys.exit(1)  # exit with code 1 if the issue is present