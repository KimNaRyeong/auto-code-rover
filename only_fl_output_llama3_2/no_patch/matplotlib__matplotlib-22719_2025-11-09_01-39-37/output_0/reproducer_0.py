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
                self.fail("Expected MatplotlibDeprecationWarning")
            except MatplotlibDeprecationWarning as e:
                print_stacktrace(e)

    def print_stacktrace(self, e: Exception):
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

if __name__ == '__main__':
    unittest.main()
