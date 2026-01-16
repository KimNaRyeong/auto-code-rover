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

def validate_parameters():
    try:
        fig, axs = plt.subplots(ncols=2)  # Expected to work
        fig.clear()
        _, ax = plt.subplots()
        ax.legend(ncol=2)  # This should pass without exceptions
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("Inconsistency detected in keyword-arguments ncol/ncols.") from None

    try:
        fig, axs = plt.subplots(nrows=2)  # Expected to work
        fig.clear()
        _, ax = plt.subplots()
        ax.legend(nrow=2)  # This should raise an exception or warning if inconsistent
        print("No inconsistency detected. Exiting without error.")
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("Inconsistency detected in keyword-arguments nrows/nrow.") from None

try:
    validate_parameters()
except AssertionError as err:
    print(err)
    exit(1)
```

This script checks for the consistency in the usage of `ncols/ncol` and `nrows/nrow` between different parts of the `matplotlib` library. It attempts to use `ncols` with `plt.subplots()` and `ncol` with `axis.legend()`, then the reverse with `nrows` and `nrow`. The presence of an `AttributeError` indicates the parameter naming is inconsistent, leading to the printing of a stack trace and raising an AssertionError.