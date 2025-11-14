Here is the reproducer script:

```python
import numpy as np
from sklearn.linear_model import RidgeClassifierCV
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestRidgeClassifierCV(unittest.TestCase):

    def test_store_cv_values(self):
        try:
            rr = RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, store_cv_values=True).fit(np.random.randn(100, 30), np.random.normal(size=100))
            self.assertTrue(True)
        except Exception as e:
            f = StringIO()
            with redirect_stdout(f):
                print_stacktrace(e)
            self.fail(f.getvalue())

if __name__ == '__main__':
    unittest.main(exit=False)
```

This script will run the test and if the `store_cv_values` flag raises a `TypeError`, it will print the stack trace and fail the test.