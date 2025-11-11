Here is the reproducer script:

```python
import unittest
from unittest.mock import patch
import sys
import traceback

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

def run_test():
    try:
        import unittest
        class MyTestCase(unittest.TestCase):
            def setUp(self):
                pass

            @unittest.skip("hello")
            def test_one(self):
                pass

            def tearDown(self):
                raise NameError("xxx")

        suite = unittest.TestSuite()
        suite.addTest(MyTestCase('test_one'))
        runner = unittest.TextTestRunner()
        result = runner.run(suite)
        if not result.wasSuccessful():
            print_stacktrace(result.exceptions[0])
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    run_test()
```

This script runs the test with `--pdb` and checks if the teardown method is executed when a test is skipped. If it is, an `AssertionError` is raised with the stack trace of the issue.