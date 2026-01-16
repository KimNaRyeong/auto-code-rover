Below is the Python script `reproducer.py` that reproduces the inconsistency issue between `ncols`/`ncol` and `nrows`/`nrow` when using Matplotlib. This script is designed to raise an `AssertionError` if it encounters inconsistency in the usage of these keyword arguments. It showcases the inconsistency by attempting to use `ncol` with `subplots` (which expects `ncols`) and `ncols` with `legend` (which expects `ncol`), or vice versa, based on current Matplotlib conventions.

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

def check_subplot_kwargs():
    try:
        # Attempt to use inconsistent keyword argument with plt.subplots
        fig, ax = plt.subplots(ncol=2)
    except TypeError as e:
        print_stacktrace(e)
        # Raising AssertionError to signal the presence of the issue
        raise AssertionError("plt.subplots() does not accept 'ncol'; 'ncols' is expected.")
    else:
        print("plt.subplots() accepted 'ncol' without error, inconsistency might have been resolved.")

def check_legend_kwargs():
    try:
        # Plot a simple line and attempt to use inconsistent keyword argument with ax.legend
        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="Line")
        ax.legend(ncols=2)
    except TypeError as e:
        print_stacktrace(e)
        # Raising AssertionError to signal the presence of the issue
        raise AssertionError("ax.legend() does not accept 'ncols'; 'ncol' is expected.")
    else:
        print("ax.legend() accepted 'ncols' without error, inconsistency might have been resolved.")

if __name__ == '__main__':
    try:
        check_subplot_kwargs()
        check_legend_kwargs()
    except AssertionError as e:
        print_stacktrace(e)
```

To execute this script, save it to a file named `reproducer.py` in the root directory of your project and run it using `python3 reproducer.py`. 

The script works by deliberately invoking each function (`plt.subplots` and `ax.legend`) with the "incorrect" keyword arguments based on the current Matplotlib API, expecting a `TypeError` due to argument inconsistency. When the inconsistency exists (meaning, if Matplotlib has not unified the keyword argument names), the specific `TypeError` is caught, and a custom `AssertionError` is raised along with a stack trace to indicate the source of the issue. 

When the inconsistency is fixed, the script will run without raising any exceptions, implying the resolution.