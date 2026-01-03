import unittest
import sys
import pytest

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

def test_mytestcase():
    mytestcase = MyTestCase()
    mytestcase.setUp()
    mytestcase.test_one = None
    with pytest.raises(AssertionError):
        mytestcase.tearDown()
    mytestcase.tearDown()

if __name__ == "__main__":
    try:
        test_mytestcase()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
