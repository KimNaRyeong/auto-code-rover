import matplotlib.pyplot as plt
from matplotlib import rcParams
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestTightLayout(unittest.TestCase):

    def test_tight_layout(self):
        with self.assertRaises(AssertionError):
            with redirect_stdout(StringIO()):
                rcParams['figure.autolayout'] = True
                fig, axes = plt.subplots(ncols=2)
                fig.tight_layout(w_pad=10)

    def test_no_stacktrace(self):
        try:
            self.test_tight_layout()
        except AssertionError as e:
            print_stacktrace(e)
            self.fail("Expected no stack trace")

if __name__ == '__main__':
    unittest.main()
