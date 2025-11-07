import unittest

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

class TestReproducer(unittest.TestCase):
    def test_reproduce_issue(self):
        # Code that reproduces the issue goes here
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    try:
        unittest.main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

