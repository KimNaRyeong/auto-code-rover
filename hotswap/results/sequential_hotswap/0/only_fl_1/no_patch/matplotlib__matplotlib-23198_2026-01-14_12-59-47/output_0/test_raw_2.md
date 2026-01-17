Given the instructions and aiming at the detection of the reported inconsistency in the Matplotlib API between `ncols`/`ncol` and `nrows`/`nrow` argument usage, a Python script needs to specifically check for this inconsistency and raise an AssertionError if the behavior does not align with expectations. Here is an attempt to directly address the inconsistency noted, aiming to raise an error intentionally to highlight the issue.

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

def test_kwargs():
    try:
        # Testing consistent keyword arg use between subplots and legend
        fig, axs = plt.subplots(nrows=1, ncols=2)
        axs[0].plot([0, 1], [0, 1], label="Line A")
        axs[1].plot([0, 1], [1, 0], label="Line B")
        
        # Forcing the following to raise an error deliberately if 'ncol' not accepted here
        try:
            fig, axs = plt.subplots(nrows=1, ncol=2)
            inconsistency = False
        except TypeError:
            inconsistency = True
        
        axs[0].legend(ncol=1)
        # Forcing the following to raise an error deliberately if 'ncols' not accepted here
        try:
            axs[1].legend(ncols=1)
            inconsistency |= False
        except TypeError:
            inconsistency |= True

        if inconsistency:
            raise AssertionError("Inconsistency detected in keyword argument usage between subplots and legend: nrows/nrow or ncols/ncol")
        else:
            print("Keyword argument usage is consistent. No issue detected.")
    
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    test_kwargs()
```

This script is designed to directly address and trigger the inconsistency issue. It first attempts to use both `ncols` in `plt.subplots()` and `ncol` in `.legend()`, which should work according to the current Matplotlib conventions. Then, it deliberately tests for the wrong usage (using `ncol` in `plt.subplots()` and `ncols` in `.legend()`) expecting to catch a `TypeError`. By this, it raises an `AssertionError` if it detects that Matplotlib does not handle these keyword arguments consistently, demonstrating that the issue is present. If the incorrect usage somehow does not raise an error, it could mean that the Matplotlib API has become fully consistent in this aspect, or that the error handling within this script needs adjustment.