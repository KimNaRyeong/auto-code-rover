Here is the standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
from sklearn.metrics import pairwise_distances

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

X = np.array([
    [1, 3],
    [2, 1],
    [3, 2]
])

try:
    result = pairwise_distances(X, metric='cosine', n_jobs=-1)
    expected_result = np.array([
        [0.         , 0.29289322, 0.21064778],
        [0.29289322, 0.         , 0.00772212],
        [0.21064778, 0.00772212, 0.        ]
    ])
    assert np.allclose(result, expected_result), "pairwise_distances returns zeros for metric cosine with n_jobs=-1"
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue not present, exiting with code 0")
exit(0)
```
This script will raise an `AssertionError` when the issue is present and print a stack trace of the issue. If the issue is fixed, it will exit with code 0.