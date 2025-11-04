Here is the reproducer script:

```python
import QQ
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        try:
            x = 0.5
            QQ.frac_field(1/x)
        except AssertionError as e:
            print_stacktrace(e)
            raise

if __name__ == "__main__":
    suite = unittest.TestSuite()
    suite.addTest(Reproducer("test_issue"))
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)

```

This script creates a test case that attempts to create a fraction field with 1/x, where x is set to 0.5. If an AssertionError is raised during this process, the script prints the stack trace and then re-raises the exception.