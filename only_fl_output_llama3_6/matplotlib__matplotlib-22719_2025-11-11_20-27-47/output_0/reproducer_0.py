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
