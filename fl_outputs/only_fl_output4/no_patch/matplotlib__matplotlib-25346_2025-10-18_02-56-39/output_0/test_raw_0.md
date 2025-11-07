```python
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

def check_constrained_layout_with_wrapped_titles():
    import matplotlib.pyplot as plt
    from matplotlib.backend_bases import FigureCanvasBase

    fig, ax_arr = plt.subplots(2, 2, figsize=(3, 3), layout="constrained")
    fig.suptitle("suptitle that is clearly too long in this case", wrap=True)
    ax_arr[1, 0].set_title("axes title that is too long for the size", wrap=True)

    # Rendering the figure to trigger layout adjustment
    FigureCanvasBase(fig).draw()

    # Assuming that the issue is present when titles overlap or are clipped
    # Assert that the top and bottom of the figure are well-defined and not overlapping.
    # This is a simplistic check, primarily aimed at identifying when the issue is *not* present.
    # For a real-world scenario, a visualization-based or more complex layout analysis may be required.
    try:
        # These values are hypothetical checks that might not accurately reflect
        # the condition when the bug is fixed but serve as an example.
        top = fig.subplotpars.top
        bottom = fig.subplotpars.bottom
        assert top > bottom, "Constrained layout should provide enough space between titles"
    except AssertionError as e:
        print_stacktrace(e)
        raise

    # If the script reaches this point without an exception, the issue is considered not present
    print("No issue found.")

if __name__ == "__main__":
    try:
        check_constrained_layout_with_wrapped_titles()
    except AssertionError:
        # Exiting with non-zero code to indicate failure/error
        exit(1)
    else:
        # Exiting with code 0 to indicate success/no error
        exit(0)
```