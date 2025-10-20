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
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_artist_after_axes_clear():
    try:
        # Step to reproduce issue for removal
        f, a = plt.subplots()
        l, = a.plot([1, 2])
        l.remove()
        if l.axes is not None:
            raise AssertionError("After removal, the artist's `.axes` attribute should be None")

        # Step to reproduce issue for clearing axes
        f, a = plt.subplots()
        l, = a.plot([1, 2])
        a.cla()
        if l.axes is not None:
            raise AssertionError("After clearing the axes, the artist's `.axes` attribute should be None")

        # If no AssertionError was raised, the issue is considered fixed
        print("Issue is fixed!")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate failure

if __name__ == "__main__":
    test_artist_after_axes_clear()
    exit(0)  # Exit with code 0 if the script runs to completion without exceptions
```

This script is designed to correctly raise an `AssertionError` when the issue described is present. In the scenario where clearing an axis with `cla()` doesn't unset the `.axes` attribute correctly, the script will catch this as an error and print a stack trace showing where the issue occurred in the script. If the `AssertionError` occurs as expected given the issue description, that means the script has successfully reproduced the issue. If for some reason the test passes (indicating the issue has been resolved or does not occur), it will print "Issue is fixed!" and exit with code 0, implying success.