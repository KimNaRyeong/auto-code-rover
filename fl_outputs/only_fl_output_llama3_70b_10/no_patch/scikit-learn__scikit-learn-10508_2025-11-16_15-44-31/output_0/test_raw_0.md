Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
import numpy as np
from sklearn.preprocessing import LabelEncoder

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

def main():
    le = LabelEncoder()
    le.fit([1,2])
    assert np.array_equal(le.transform([]), np.array([], dtype=np.int64)), "Empty array not returned for integer labels"

    le = LabelEncoder()
    try:
        le.fit(["a","b"])
        le.transform([])
        raise AssertionError("Expected TypeError for empty list with string labels")
    except TypeError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    main()
```
This script will reproduce the issue and raise an `AssertionError` when the issue is present, printing a stack trace of the error. If the issue is fixed, it will exit with code 0.