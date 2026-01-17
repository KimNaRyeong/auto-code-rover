```python
# reproducer.py
import matplotlib
matplotlib.use('Qt5Agg')  # Set backend for consistency

from matplotlib import pyplot as plt
from matplotlib.widgets import SpanSelector
import sys

class TestSpanSelector:
    def __init__(self):
        self.span_removed = False

    def onselect(self, vmin, vmax):
        if vmin == vmax:  # Detects a click without drag (removal of span)
            self.span_removed = True
            print(f"Span removed at {vmin}")
        else:
            print(f"Span selected from {vmin} to {vmax}")

    def test_spanselector(self):
        fig, ax = plt.subplots()
        ax.plot([10, 20], [10, 20])
        self.span_selector = SpanSelector(ax, self.onselect, "horizontal", interactive=True)
        plt.show()

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

if __name__ == "__main__":
    test = TestSpanSelector()
    try:
        test.test_spanselector()

        # Verify if span was removed, should raise an error if the issue is present
        assert test.span_removed, "Span removal was not detected."
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

    print("No issue detected.")
    sys.exit(0)
```

This standalone Python file `reproducer.py` is intended to be placed at the root directory of the project and executed to reproduce the described issue. When you run `python3 reproducer.py`, it utilizes the Matplotlib's SpanSelector widget with a plot. The SpanSelector is supposed to invoke the `onselect` callback when it is interactively removed by clicking without dragging (click-release, where `vmin == vmax`). The script sets up a class to manage the test and tracks if a span removal (click-release) is correctly detected and reported. 

If the issue is present (i.e., the `onselect` callback is not called upon an "empty" click leading to `vmin == vmax`), the script will raise an `AssertionError` and print a stacktrace clearly showing where the issue occurred. If the issue has been fixed and the script correctly detects a span removal, it will exit with code 0, indicating no issue was detected.