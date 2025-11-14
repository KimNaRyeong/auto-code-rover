Here is the standalone Python file `reproducer.py` to reproduce the issue:
```
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

try:
    sample = np.full([10_000_000, 1], 10.0, dtype=np.float16)
    scaler = StandardScaler()
    result = scaler.fit_transform(sample)
    if np.isnan(result).any():
        raise AssertionError("StandardScaler fit overflows on float16")
except Exception as e:
    print_stacktrace(e)
    exit(1)

exit(0)
```
This script creates a large `float16` numpy array, attempts to fit and transform it using `StandardScaler`, and checks if the result contains any NaN values. If it does, it raises an `AssertionError` with a stack trace of the issue. If no exception is raised, the script exits with code 0.