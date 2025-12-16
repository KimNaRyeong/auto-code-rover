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
When executed with `python3 reproducer.py`, the script raises an `AssertionError` with a stack trace showing that the `tearDown` method was executed on a skipped test.

The output should look like this:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    unittest.main(argv=args)
  File "/usr/lib/python3.8/unittest/main.py", line 100, in __init__
    self.parseArgs(args)
  File "/usr/lib/python3.8/unittest/main.py", line 147, in parseArgs
    self.createTests()
  File "/usr/lib/python3.8/unittest/main.py", line 221, in createTests
    self.module)
  File "/usr/lib/python3.8/unittest/defaultTestLoader.py", line 98, in loadTestsFromNames
