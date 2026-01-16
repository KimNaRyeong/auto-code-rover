```python
# reproducer.py
import matplotlib
matplotlib.use('Qt5Agg')  # Ensuring the backend is set accordingly

from matplotlib import pyplot as plt
from matplotlib.widgets import SpanSelector

# Global variable to store the span selector output
span_selector_output = []

def onselect(vmin, vmax):
    """
    Callback function to capture the output from the SpanSelector.
    It stores the vmin and vmax values into the global list.
    """
    global span_selector_output
    span_selector_output.append((vmin, vmax))

def simulate_click_and_drag(ax, xstart, ystart, xend, yend):
    """
    Simulates a mouse click and drag event on the given Axes.
    """
    from matplotlib.backend_bases import MouseEvent, MouseButton

    # Simulate the mouse button being pressed
    ax.figure.canvas.button_press_event(xstart, ystart, MouseButton.LEFT, guiEvent=None)

    # Simulate the mouse movement
    ax.figure.canvas.motion_notify_event(xend, yend, guiEvent=None)

    # Simulate the mouse button being released
    ax.figure.canvas.button_release_event(xend, yend, MouseButton.LEFT, guiEvent=None)

def simulate_click(ax, x, y):
    """
    Simulates a mouse click event on the given Axes.
    """
    from matplotlib.backend_bases import MouseEvent, MouseButton

    # Simulate the mouse button being pressed and immediately released at the same position
    ax.figure.canvas.button_press_event(x, y, MouseButton.LEFT, guiEvent=None)
    ax.figure.canvas.button_release_event(x, y, MouseButton.LEFT, guiEvent=None)

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

def test_spanselector_notify():
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])
    ss = SpanSelector(ax, onselect, "horizontal", interactive=True)
    plt.show(block=False)  # To ensure the plot doesn't block the script

    # Simulate a span selection
    simulate_click_and_drag(ax, 10, 15, 20, 15)
    # Simulate a click (which should remove the selector)
    simulate_click(ax, 15, 15)

    # Allow time for the events to be processed
    plt.pause(1)

    assert len(span_selector_output) == 2, "SpanSelector did not notify removal by empty click"

try:
    test_spanselector_notify()
except AssertionError as e:
    print_stacktrace(e)
    plt.close('all')  # Close the plot
    exit(1)  # Exit with error code to indicate failure
else:
    plt.close('all')  # Ensure to close the plot on success as well
    print("Success: The issue is not present or has been fixed.")
    exit(0)
```