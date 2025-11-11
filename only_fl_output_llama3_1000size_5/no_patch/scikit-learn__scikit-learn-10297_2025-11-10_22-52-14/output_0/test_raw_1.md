The issue seems to be related to the installation of scikit-learn. The error message suggests that the package has not been built correctly.

Here is a new reproducer script:

```python
import numpy as np
from sklearn.linear_model import RidgeClassifierCV
import unittest
from io import StringIO
from contextlib import redirect_stdout

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

class TestRidgeClassifierCV(unittest.TestCase):

    def test_store_cv_values(self):
        try:
            rr = RidgeClassifierCV(alphas=np.arange(0.1, 1000, 0.1), normalize=True, store_cv_values=True).fit(np.random.randn(100, 30), np.random.normal(size=100))
            self.assertTrue(True)
        except Exception as e:
            print_stacktrace(e)
            raise

if __name__ == '__main__':
    unittest.main(exit=False)
```

This script will run the test and if the `store_cv_values` flag raises a `TypeError`, it will print the stack trace and then re-raise the exception.