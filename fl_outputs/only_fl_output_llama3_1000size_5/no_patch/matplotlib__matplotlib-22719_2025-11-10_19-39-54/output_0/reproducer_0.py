import matplotlib.pyplot as plt
import unittest
from io import StringIO
from contextlib import redirect_stdout

class TestReproducer(unittest.TestCase):

    def test_reproducer(self):
        f, ax = plt.subplots()
        ax.xaxis.update_units(["a", "b"])
        with redirect_stdout(StringIO()):
            try:
                ax.plot([], [])
                self.assertFalse(True, 'Expected AssertionError')
            except AssertionError as e:
                print_stacktrace(e)

if __name__ == '__main__':
    unittest.main()
