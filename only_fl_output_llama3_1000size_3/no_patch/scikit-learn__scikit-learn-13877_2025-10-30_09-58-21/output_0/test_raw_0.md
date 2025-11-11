Here is the reproducer script:

```python
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import normalize

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

This script will run the `pairwise_distances` function with `metric='cosine'` and `n_jobs=-1`, and then check if all values in the result are zero. If they are, it will print a stack trace of the assertion error and exit with code 1.