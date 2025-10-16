```python
import matplotlib.pyplot as plt
import sys

def assert_offset_text_color():
    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot([1.01e9,1.02e9,1.03e9])
    plt.draw()  # Force drawing to apply all updates and calculate the offset text

    # Fetching the configured label colors and the actual offset text color
    labelcolor_y = plt.rcParams.get('ytick.labelcolor', 'black')
    offset_text_color = ax.yaxis.get_offset_text().get_color()
    
    # Asserting that the offset text color should match the ytick.labelcolor
    assert offset_text_color == labelcolor_y, "Offset text color does not match ytick.labelcolor configuration."

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

if __name__ == "__main__":
    plt.rcParams.update({'ytick.labelcolor': 'red'})
    try:
        assert_offset_text_color()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)  # Exit with error code 1 to indicate the assertion failed (issue is present)
    sys.exit(0)  # Exit with code 0 when no issue is found (issue is fixed)
```

This script, placed in the root directory of a project using Matplotlib, will check if the bug described is present. Specifically, it verifies that the color of the offset text on the y-axis matches the configured `ytick.labelcolor`. If the colors match, the script exits silently with code 0, indicating no issues. If not, it raises an `AssertionError` and prints a detailed stack trace to help trace the source of the problem, then exits with code 1.