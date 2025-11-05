import matplotlib.pyplot as plt
import matplotlib as mpl
from unittest import TestCase

class Reproducer(TestCase):
    def test_issue(self):
        mpl.rcParams['figure.autolayout'] = True
        fig, axes = plt.subplots(ncols=2)
        fig.tight_layout(w_pad=10)  # This should raise an AssertionError
        self.fail("Expected AssertionError")

if __name__ == '__main__':
    try:
        Reproducer().test_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue not present")
        exit(0)

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

