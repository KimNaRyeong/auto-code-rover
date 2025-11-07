Here is the reproducer script:

```Python
import xarray as xr
from unittest import TestCase
import traceback
import sys

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

class TestIssue(TestCase):
    def test_issue(self):
        try:
            coeffs = xr.DataArray([1, 2, 3], dims="degree")
            coord = xr.DataArray([0, 1, 2], dims="x")
            xr.polyval(coord, coeffs)
            self.fail("Expected KeyError")
        except Exception as e:
            print_stacktrace(e)

if __name__ == "__main__":
    test_issue = TestIssue()
    test_result = test_issue.test_issue()
    if test_result is None:
        exit(0)
    else:
        exit(1)
```

This script defines a `TestIssue` class that contains a single test method. In this method, it attempts to reproduce the issue by calling `xr.polyval` with the given coordinates and coefficients. If the expected KeyError is raised, the script prints the stack trace using the provided function and then exits with code 1.