Here is the reproducer script:

```python
import numpy as np
from sklearn.metrics.cluster import davies_bouldin_score
from sklearn.datasets import make_blobs
import unittest

class TestDaviesBouldinScore(unittest.IsolatedTestCase):
    def test_davies_bouldin_score(self):
        X, y = make_blobs(n_samples=100, centers=2, cluster_std=1.5, random_state=0)
        with self.assertRaises(RuntimeWarning):
            davies_bouldin_score(X, y)

if __name__ == '__main__':
    unittest.main()
```

This script uses the `make_blobs` function from scikit-learn to generate a dataset with two clusters and then calls the `davies_bouldin_score` function on this dataset. It expects the function to raise a `RuntimeWarning` due to division by zero, which is what happens when you run the original code.

Please note that you need to have scikit-learn installed in your Python environment for this script to work.