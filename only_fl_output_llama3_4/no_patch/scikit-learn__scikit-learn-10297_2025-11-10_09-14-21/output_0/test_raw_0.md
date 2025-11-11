Here is the reproducer script:

```python
import numpy as np
from sklearn.linear_model import RidgeClassifierCV
import unittest
from io import StringIO
import sys
import traceback

def print_stacktrace(e):
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
        except TypeError as e:
            print_stacktrace(e)
            self.fail("Expected no error")
        else:
            raise AssertionError("Expected TypeError")

if __name__ == '__main__':
    unittest.main()
```

You can run this script with `python3 reproducer.py` to reproduce the issue.