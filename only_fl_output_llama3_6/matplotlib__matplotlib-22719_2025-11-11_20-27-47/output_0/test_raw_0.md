Here is the reproducer script:

```python
import matplotlib.pyplot as plt
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestIssue(unittest.TestCase):

    def test_issue(self):
        f, ax = plt.subplots()
        ax.xaxis.update_units(["a", "b"])
        with redirect_stdout(StringIO()):
            try:
                ax.plot([], [])
                self.fail("Expected MatplotlibDeprecationWarning")
            except MatplotlibDeprecationWarning as e:
                print_stacktrace(e)
                self.assertTrue(True)

    def test_issue_with_conversion(self):
        f, ax = plt.subplots()
        ax.xaxis.update_units(["a", "b"])
        with redirect_stdout(StringIO()):
            try:
                ax.convert_xunits([])
                self.fail("Expected MatplotlibDeprecationWarning")
            except MatplotlibDeprecationWarning as e:
                print_stacktrace(e)
                self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()
```

This script will run two tests: `test_issue` and `test_issue_with_conversion`. Each test attempts to reproduce the issue by calling `ax.plot([], [])` or `ax.convert_xunits([])`, respectively. If the issue is present, it should raise a `MatplotlibDeprecationWarning` and print the stack trace.