 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import unittest
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

class MyTestCase(unittest.TestCase):
    def setUp(self):
        pass

    @unittest.skip("hello")
    def test_one(self):
        pass

    def tearDown(self):
        raise AssertionError("tearDown should not be executed on skipped tests")

if __name__ == "__main__":
    try:
        # Run the test case
        suite = unittest.TestLoader().loadTestsFromTestCase(MyTestCase)
        unittest.TextTestRunner(verbosity=2).run(suite)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To reproduce the issue, run the script with `pytest` and the `--pdb` option:
```
$ python3 -m pytest --pdb reproducer.py
```
This should raise an `AssertionError` with a stack trace that shows the `tearDown` method being executed on a skipped test.

If you want to test the behavior with a different version of `pytest`, you can modify the script to use a specific version of `pytest` by changing the first line to:
```python
import sys; sys.path.insert(0, '/path/to/pytest-5.4.1')
```
Replace `/path/to/pytest-5.4.1` with the actual path to the `pytest` package that you want to use.