```python
# reproducer.py

import matplotlib.pyplot as plt

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', line_number, ":", code_context, file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_clear_and_remove():
    try:
        # Test case 1: Removing the artist from its axes.
        f, a = plt.subplots(); l, = a.plot([1, 2]); l.remove()
        assert l.axes is None, "Artist's `.axes` attribute should be None after removal."

        # Test case 2: Clearing the axes.
        f, a = plt.subplots(); l, = a.plot([1, 2]); a.cla()
        assert l.axes is None, "Artist's `.axes` attribute should be None after axes are cleared."
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_clear_and_remove()
    except AssertionError:
        # If an AssertionError is caught, exit with a non-zero status to indicate failure.
        exit(1)
    # If no exception is caught, exit with zero status to indicate success.
    exit(0)
```