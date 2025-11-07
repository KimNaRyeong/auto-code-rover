Here is the reproducer script:

```python
import numpy as np
from sklearn.metrics import pairwise_distances
import traceback
import sys

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
    X = np.array([
        [1, 3],
        [2, 1],
        [3, 2]
    ])
    
    try:
        result = pairwise_distances(X, metric='cosine', n_jobs=-1)
        assert not np.allclose(result, 0), "pairwise_distances returns zeros for metric cosine when executed in parallel"
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the `pairwise_distances` function with the given input and check if the result is not all zeros. If it's not, then the issue is present and an `AssertionError` will be raised. The stack trace of the error will be printed to the console.