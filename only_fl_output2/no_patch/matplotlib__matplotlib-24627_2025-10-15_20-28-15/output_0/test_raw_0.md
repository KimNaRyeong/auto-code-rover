```python
import matplotlib.pyplot as plt

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

def test_issue():
    try:
        # Test case where artist is removed and axes should be unset
        f, a = plt.subplots(); l, = a.plot([1, 2]); l.remove()
        assert l.axes is None, "Artist's `.axes` attribute not unset after removal"

        # Test case where axes are cleared and artist's axes should be unset
        f, a = plt.subplots(); l, = a.plot([1, 2]); a.cla()
        assert l.axes is None, "Artist's `.axes` attribute not unset after axes are cleared"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_issue()
    except AssertionError:
        # An AssertionError means the issue is present.
        exit(1)  # Non-zero exit code indicates failure/reproduction of the issue.
    print("Issue is fixed, or could not reproduce the issue.")
    exit(0)  # Exit with code 0 to indicate success/non-reproduction.
```