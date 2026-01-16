```python
# reproducer.py
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances
from scipy.spatial.distance import cdist
import sklearn

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

def test_euclidean_distances_behavior():
    # Using a predefined random seed to ensure reproducibility
    np.random.seed(42)
    # Generating a random array similar to the provided size (100,10000) with float32
    X = np.random.rand(100, 10000).astype(np.float32)
    
    # Computing distances using sklearn and scipy
    ed_sklearn = euclidean_distances(X)
    ed_scipy = cdist(X, X, metric='euclidean')
    
    # Asserting that no entries are 0 and everything behaves as expected
    if np.any(ed_sklearn <= 0) or not np.allclose(ed_sklearn, ed_scipy, atol=1e-6):
        raise AssertionError("Euclidean distances in sklearn differ significantly from scipy's cdist.")

try:
    test_euclidean_distances_behavior()
except AssertionError as e:
    print_stacktrace(e)
    # Exiting with a non-zero code to indicate failure
    exit(1)
else:
    print(f"No issues found with sklearn {sklearn.__version__}. Euclidean distances computation behaves as expected.")
    # Exiting with zero to indicate success
    exit(0)
```