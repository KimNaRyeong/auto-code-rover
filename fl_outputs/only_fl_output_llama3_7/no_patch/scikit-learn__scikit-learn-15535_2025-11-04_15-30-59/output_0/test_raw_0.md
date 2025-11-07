Here is the reproducer script:

```python
import unittest
from sklearn.metrics.cluster import mutual_info_score
import numpy as np
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

class TestReproducer(unittest.TestCase):

    def test_reproduce_issue(self):
        try:
            x = np.random.choice(['a', 'b'], size=20).astype(object)
            mutual_info_score(x, x)
        except Exception as e:
            print_stacktrace(e)
            self.fail()

        try:
            x = np.random.choice(['a', 'b'], size=20)
            mutual_info_score(x, x)
        except Exception as e:
            print_stacktrace(e)
            self.fail()

    def test_issue_fixed(self):
        try:
            x = np.random.choice(['a', 'b'], size=20).astype(object)
            mutual_info_score(x, x)
        except AssertionError:
            pass
        else:
            raise AssertionError("Issue not fixed")

        try:
            x = np.random.choice(['a', 'b'], size=20)
            mutual_info_score(x, x)
        except AssertionError:
            pass
        else:
            raise AssertionError("Issue not fixed")

if __name__ == '__main__':
    unittest.main()
```

This script will run the tests and if any of them fail (i.e., an exception is raised), it will print the stack trace and exit with code 1. If all tests pass, it will exit with code 0.