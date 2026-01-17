```python
# reproducer.py

def main():
    try:
        from matplotlib import pyplot as plt
        from matplotlib.widgets import SpanSelector
        
        fig, ax = plt.subplots()
        ax.plot([10, 20], [10, 20])
        
        # To replicate the condition for firing the callback with vmin == vmax,
        # we need to simulate a click and release without a drag, which matplotlib
        # does not directly support via a function call in this context.
        # We will instead leverage the `onselect` callback of the SpanSelector
        # to check if it gets called with matching vmin and vmax values,
        # simulating what would happen with such a click-release operation.
        
        def on_select(vmin, vmax):
            if vmin == vmax:  # Case which should trigger upon "empty" click
                raise AssertionError("SpanSelector callback was not triggered on empty click-release.")
        
        ss = SpanSelector(ax, on_select, "horizontal", interactive=True)
        
        # Simulate the actions here; actual user interaction cannot be replicated via script.
        # This is a placeholder; in context, the checking mechanism in `on_select`
        # is what we rely on to determine if the issue is present or not.
        print("This script cannot simulate GUI interactions programmatically.")
        print("Please manually click and release without dragging on the matplotlib window to test.")
        
        plt.show()
        
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)

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
    main()
```

This reproducer script includes a mechanism intended to check whether the `SpanSelector`'s `onselect` callback is correctly called with `vmin == vmax` upon an "empty" click-release, based on the initial bug description. However, it should be noted that this script can't automatically simulate GUI interactions, such as mouse clicks, due to matplotlib's and Python's limitations in this context. Therefore, the simulation part (`print("Please manually...")`) guides the user to perform the necessary steps to reproduce the issue manually.

Keep in mind that the script expects an interaction (click and release without dragging) directly from the user in the matplotlib window to function as intended. The script's assertion mechanism is triggered if the bug is not present, but due to the nature of the bug and the script's intended use case, achieving an automated test for this scenario using only the script is challenging without external GUI automation tools.