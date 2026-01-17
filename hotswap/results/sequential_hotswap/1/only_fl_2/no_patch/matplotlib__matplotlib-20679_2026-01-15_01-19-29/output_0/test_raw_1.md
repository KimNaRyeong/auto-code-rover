To address the requirements and constraints mentioned, an attempt to automate the reproduction of the issue within the capabilities of a script could involve simulating user interaction via event generation directly in the Matplotlib event loop. However, it's important to understand that truly automating GUI interactions, like clicks without a mouse, is quite challenging without resorting to external GUI automation tools.

The following `reproducer.py` tries to simulate a click within the Matplotlib canvas by programmatically generating and triggering the mouse press and release events at the same coordinates, aiming to mimic an "empty click" which should trigger the `onselect` callback with `vmin == vmax`. Note that due to the nature of GUI frameworks and event processing, this method might not precisely mimic actual user interactions and could behave differently depending on the environment and Matplotlib backend used.

```python
import matplotlib.pyplot as plt
from matplotlib.widgets import SpanSelector
import numpy as np


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

def simulate_click(ax, x, y):
    """Simulate a click at the given x, y coordinates in the axes."""
    canvas = ax.figure.canvas

    # Create a MouseEvent for clicking
    event_press = matplotlib.backend_bases.MouseEvent(
        name='button_press_event',
        canvas=canvas,
        x=x, y=y,
        button=1,
        key=None
    )
    event_release = matplotlib.backend_bases.MouseEvent(
        name='button_release_event',
        canvas=canvas,
        x=x, y=y,
        button=1,
        key=None
    )

    # Trigger the mouse press and release events
    canvas.callbacks.process('button_press_event', event_press)
    canvas.callbacks.process('button_release_event', event_release)

def onselect(vmin, vmax):
    assert vmin != vmax, "Selector removed without span (vmin == vmax). Issue is present."

fig, ax = plt.subplots()
ax.plot(np.random.rand(10))

span_stays = True  # Change based on the version and test case
selector = SpanSelector(ax, onselect, "horizontal",
                        useblit=True,
                        span_stays=span_stays,
                        interactive=True)

# Assuming a figure size and a reasonable click position,
# these coordinates might need adjustment based on actual figure and DPI settings.
simulate_click(ax, 100, 200)

try:
    plt.show()
except Exception as e:
    print_stacktrace(e)
```

**Caveats and Limitations:**

1. **Backend-Specific Behavior:** The script's effectiveness can vary based on the matplotlib backend in use because GUI backends handle events differently. If the script does not work as expected, verify it against the backend reported in the issue (in this case, `qt5agg`).

2. **Event Simulation Accuracy:** While the script attempts to simulate mouse click events programmatically, the difference in event context (like the event's metadata and timing) may not replicate the subtle nuances of actual GUI interactions perfectly. Hence, manual verification might still be needed.

3. **Environment and Configuration:** The script assumes a standard environment and may require adaptations for specific configurations or if the plotting window's size and DPI affect expected coordinates for mouse events.

The script attempts to automatically reproduce the issue under discussion by simulating mouse events that should lead to the issue condition if present. However, due to the outlined limitations, this approach might not fully substitute for user-based manual testing in all cases.