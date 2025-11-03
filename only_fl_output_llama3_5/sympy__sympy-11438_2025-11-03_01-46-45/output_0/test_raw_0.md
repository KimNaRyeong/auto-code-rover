Here is the reproducer script:

```python
import diophantine
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        eq = x**2+y**2+z**4-(1+4+2**4)
        try:
            classify_diop(eq)
            self.fail("Expected AssertionError")
        except AssertionError as e:
            print_stacktrace(e)

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Reproducer('test_issue'))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
```

This script defines a test case `test_issue` that attempts to reproduce the issue. It calls the `classify_diop` function with the given equation and expects an AssertionError to be raised. If the assertion is successful, it fails the test. The script then runs the test using the unittest framework and exits with code 1 if the test fails.