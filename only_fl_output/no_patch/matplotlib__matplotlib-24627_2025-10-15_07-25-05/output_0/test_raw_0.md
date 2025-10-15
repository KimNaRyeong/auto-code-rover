```python
import matplotlib.pyplot as plt

def main():
    try:
        # Scenario 1: Removing an artist unsets its `.axes` attribute
        f1, a1 = plt.subplots()
        l1, = a1.plot([1, 2])
        l1.remove()
        assert l1.axes is None, "After l1.remove(), l1.axes should be None"

        # Scenario 2: Clearing axes does not unset the `.axes` attribute of its children artists
        f2, a2 = plt.subplots()
        l2, = a2.plot([1, 2])
        a2.cla()  # Clear the axes
        assert l2.axes is None, "After a2.cla(), l2.axes should be None"
        
    except AssertionError as e:
        print_stacktrace(e)
        raise

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

This script includes checks for both of the described problematic behaviors. It asserts that after an artist is removed or the axes are cleared, the `.axes` property of the artist should be `None`. If the issue is present, the script will raise an `AssertionError` and print out a detailed stack trace, as requested. When the issue is fixed, the script will quietly complete with an exit code of 0.