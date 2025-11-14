I apologize for the mistake. Here is a new `reproducer.py` file that reproduces the issue:
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
    le.fit([1, 2])
    
    try:
        result1 = le.transform([])
        assert isinstance(result1, np.ndarray) and len(result1) == 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("LabelEncoder transform fails for empty lists (int case)")
    
    le.fit(["a", "b"])
    
    try:
        result2 = le.transform([])
        assert isinstance(result2, np.ndarray) and len(result2) == 0
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("LabelEncoder transform fails for empty lists (str case)")

if __name__ == "__main__":
    main()
```
This script will reproduce the issue by fitting a `LabelEncoder` with both integer and string labels, and then attempting to transform an empty list. If the issue is present, it will raise an `AssertionError` and print the stack trace of the exception. If the issue is fixed, the script will exit with code 0.