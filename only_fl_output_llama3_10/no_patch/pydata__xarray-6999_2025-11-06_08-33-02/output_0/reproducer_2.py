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

try:
    import xarray as xr
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected no exception") from e

if __name__ == '__main__':
    try:
        import unittest
        class TestRenameVars(unittest.TestCase):
            def test_rename_vars(self):
                try:
                    # your code here
                    pass
                except Exception as e:
                    print_stacktrace(e)
                    self.fail("Expected no exception")
        unittest.main()
    except SystemExit as e:
        if e.code != 0:
            raise AssertionError("Test failed with non-zero exit code") from e
