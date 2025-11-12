Here is the reproducer script:

```py
import numpy as np
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
    X = np.random.rand(100, 10)  # Replace with your data
    y = np.random.randint(0, 2, size=100)  # Replace with your labels

    try:
        _, X_sub, _, y_sub = train_test_split(X, y, stratify=y, train_size=None, test_size=60)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue should be reproduced"

if __name__ == "__main__":
    reproduce_issue()
```

This script attempts to subsample the data using `train_test_split` with a stratified split. If an exception is raised (which it should be), the script prints the stack trace and asserts that the issue was not fixed, causing the program to exit with code 1.