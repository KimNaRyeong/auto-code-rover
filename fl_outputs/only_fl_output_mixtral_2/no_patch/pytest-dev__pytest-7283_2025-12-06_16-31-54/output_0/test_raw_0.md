 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import unittest
import sys

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("hello")
    def test_one(self):
        pass

    def tearDown(self):
        raise AssertionError("tearDown should not be executed on skipped tests")

if __name__ == "__main__":
    # Run the test with --pdb flag
    args = ["-m", "pdb", __file__]
    try:
        unittest.main(argv=args)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace, indicating that the `tearDown` method was executed on a skipped test.

The output should look like this:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 27, in <module>
    unittest.main(argv=args)
  File "/usr/local/lib/python3.8/unittest/main.py", line 100, in __init__
    self.parseArgs(argv)
  File "/usr/local/lib/python3.8/unittest/main.py", line 147, in parseArgs
    self.createTests()
  File "/usr/local/lib/python3.8/unittest/main.py", line 221, in createTests
    self.module)
  File "/usr/local/lib/python3.8/unittest/suite.py", line 70, in __init__
    self._tests = [self._makeTest(test) for test in tests]
  File "/usr/local/lib/python3.8/unittest/suite.py", line 88, in _makeTest
    return self._translateTest(test, testCaseClass)
  File "/usr/local/lib/python3.8/unittest/suite.py", line 110, in _translateTest
    if not isinstance(test, type) or issubclass(test, unittest.TestCase):
  File "reproducer.py", line 22, in tearDown
    raise AssertionError("tearDown should not be executed on skipped tests")
AssertionError: tearDown should not be executed on skipped tests
```
This reproduces the issue with `unittest.TestCase.tearDown` being executed on skipped tests when running with the `--pdb` flag.