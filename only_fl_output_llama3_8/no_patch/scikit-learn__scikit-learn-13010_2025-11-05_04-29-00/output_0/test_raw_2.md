Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

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
    sample = np.full([10_000_000, 1], 10.0, dtype=np.float16)
    try:
        StandardScaler().fit_transform(sample)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected overflow error"

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. The script should also exit with code 0 when the issue is fixed.

To run this script, save it to a file named `reproducer.py`, then execute it using `python3 reproducer.py`.