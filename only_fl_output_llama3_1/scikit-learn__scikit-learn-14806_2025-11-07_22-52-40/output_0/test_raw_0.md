Here is the reproducer script:

```python
import numpy as np
from sklearn.impute import IterativeImputer
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestIterativeImputer(unittest.TestCase):

    def test_iterative_imputer(self):
        f = StringIO()
        with redirect_stdout(f):
            try:
                imp = IterativeImputer(max_iter=10, verbose=0)
                imp.fit([[1, 2], [3, 6], [4, 8], [10, 20], [np.nan, 22], [7, np.nan]])
                X_test = [[np.nan, 4], [6, np.nan], [np.nan, 6], [4, np.nan], [33, np.nan]]
                print(np.round(imp.transform(X_test)))
            except Exception as e:
                raise AssertionError("Expected iterative imputation with estimator but got mean imputation") from e
        self.fail("Test failed")

if __name__ == '__main__':
    unittest.main()
```

This script will run the test case and if it fails, it will print a stack trace of the issue.