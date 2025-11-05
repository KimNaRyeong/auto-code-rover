Here is the reproducer script:

```python
import numpy as np
from sklearn.decomposition import SparsePCA
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestSparsePCAIssue(unittest.TestCase):

    def test_sparse_pca_issue(self):
        train = get_data(1000, 1)
        spca = SparsePCA(max_iter=20)
        results_train = spca.fit_transform(train)

        test = get_data(10, 1)
        results_test = spca.transform(test)

        self.assertTrue(np.allclose(results_train.mean(), results_test.mean()))
        self.assertTrue(np.allclose(results_train.max(), results_test.max()))
        self.assertTrue(np.allclose(results_train.min(), results_test.min()))

    def get_data(count, seed):
        np.random.seed(seed)
        col1 = np.random.random(count)
        col2 = np.random.random(count)

        data = np.hstack([a[:,np.newaxis] for a in [
            col1 + .01*np.random.random(count),
            -col1 + .01*np.random.random(count),
            2*col1 + col2 + .01*np.random.random(count),
            col2 + .01*np.random.random(count),
        ]])
        return data

if __name__ == '__main__':
    with redirect_stdout(StringIO()):
        unittest.main()
```

This script will run the test case and check if the mean, max, and min values of the training and testing results are close. If they are not close, it means that the issue is present and an `AssertionError` will be raised.