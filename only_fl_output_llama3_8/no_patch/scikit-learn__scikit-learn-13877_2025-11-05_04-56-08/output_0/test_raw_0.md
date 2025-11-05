Here is the reproducer script:

```python
import numpy as np
from sklearn.metrics import pairwise_distances
from sklearn.preprocessing import normalize
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class TestPairwiseDistances(unittest.TestCase):

    def test_pairwise_distances(self):
        X = np.array([
            [1, 3],
            [2, 1],
            [3, 2]
        ])
        
        try:
            pairwise_distances(X, metric='cosine', n_jobs=-1)
        except Exception as e:
            print_stacktrace(e)
            self.fail("pairwise_distances returned zeros for metric cosine when executed in parallel")

if __name__ == '__main__':
    unittest.main()
```

This script will run the test and if the issue is present, it will print the stack trace of the error.