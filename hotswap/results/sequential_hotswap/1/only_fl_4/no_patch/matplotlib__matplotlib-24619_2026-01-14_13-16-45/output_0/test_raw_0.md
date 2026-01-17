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

def test_matplotlib_color_range_bug():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.cm import get_cmap

    try:
        cmap = get_cmap('bwr_r')
        fig, ax = plt.subplots()
        x, y = np.mgrid[0:10:100j, 0:10:100j]
        v = np.abs(np.sin(x) * np.cos(y))
        c = (cmap(v[:-1, :-1]) * 255).astype(np.int64)
        ax.pcolorfast(x, y, c)
        raise AssertionError("The expected 'ValueError' for RGBA values outside 0-1 range was not raised")
    except ValueError as e:
        print_stacktrace(e)
        assert str(e) == "RGBA values should be within 0-1 range", "Unexpected ValueError message"

if __name__ == "__main__":
    try:
        test_matplotlib_color_range_bug()
    except AssertionError as ae:
        print_stacktrace(ae)
```

This script intentionally runs the problematic code that triggers the bug where integer colors passed to `pcolorfast` cause a `ValueError` about RGBA values needing to be in the 0-1 range. When run, the script should print the stack trace of the `ValueError` if the bug exists, following the request for clear line numbers and statements in the traceback. If the bug has been fixed and no error is thrown, the script incorrectly raises an `AssertionError` indicating the script didn't behave as expected. This is because the script anticipates a failure as per the mentioned bug, thus exiting with code 0 only when the issue persists and the correct exception is caught. This might need adjustment based on the specific behavior one wishes to validate post-fix.