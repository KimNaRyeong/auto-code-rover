Here is the reproducer script:

```python
import numpy as np
from astropy.table import Table, QTable

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
    events = [{"A":0,"B":0, "C":np.array([], dtype=np.uint64)},
              {"A":1,"B":0, "C":np.array([], dtype=np.uint64)},
              {"A":2,"B":2, "C":np.array([0,1], dtype=np.uint64)}]
    try:
        QTable(rows=events[:2])
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script creates a list of events with arrays in the "C" field. It then tries to create a `QTable` object using the first two events, which should trigger the issue. The `print_stacktrace` function is used to print the stack trace when an exception occurs.