To address the issue where the SpanSelector does not notify when the selector is removed by an "empty" click, we need a script that accurately reproduces the scenario and checks whether the expected callback is invoked. Below is a Python script intended for this purpose. This script does not depend on Qt and uses Matplotlib's own event simulation methods to generate the clicks and drags necessary to test the SpanSelector's behavior.

This approach sidesteps the need for an actual GUI backend to be available, enabling the test to run in a headless environment if necessary. Note, however, that for visual backends and interactive use, dependencies like PyQt5 or PySide2 might still be required.

```python
# reproducer.py
import sys
import matplotlib
matplotlib.use('Agg')  # Use the 'Agg' backend for headless environments

from matplotlib import pyplot as plt
from matplotlib.widgets import SpanSelector

# Tracks whether the callback is invoked
callback_invoked = False

def onselect(vmin, vmax):
    global callback_invoked
    # Set flag to True if callback is triggered
    callback_invoked = True
    print(f"onselect called with vmin={vmin}, vmax={vmax}")

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    fig, ax = plt.subplots()
    ax.plot([10, 20], [10, 20])

    # Creating a SpanSelector that is supposed to fire on an "empty" click
    ss = SpanSelector(ax, onselect, 'horizontal', interactive=True)

    # Simulate click without drag (empty click)
    fig.canvas.button_press_event(15, 15, 1)  # x=15, y=15, button=1 (left click)
    fig.canvas.button_release_event(15, 15, 1)  # Same coordinates, indicating no drag

    # Check if the callback was invoked
    if not callback_invoked:
        print("ERROR: Callback not invoked on empty click.")
        sys.exit(1)
    else:
        print("SUCCESS: Callback correctly invoked on empty click.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
    else:
        sys.exit(0)
```

Important Notes:

- This script sets Matplotlib to use the 'Agg' backend with `matplotlib.use('Agg')` for headless operation. This is to ensure that the script can run without needing a display environment. For interactive use or in environments where a display server is available, this line should be adjusted or removed to use the default backend.
  
- The script simulates a click without drag by issuing a `button_press_event` and a `button_release_event` at the same position and checks if this triggers the `onselect` callback.

- Since we're simulating user interaction programmatically, the actual user interface will not show up. This is intended for automated testing purposes.

- If the span selector behavior has been corrected or worked as expected, the script should exit with a status code of `0`. Otherwise, it exits with `1`, indicating the issue is present.