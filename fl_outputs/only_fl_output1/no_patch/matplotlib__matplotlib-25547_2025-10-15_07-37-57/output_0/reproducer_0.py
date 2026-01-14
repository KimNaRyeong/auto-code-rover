import numpy as np
import matplotlib.pyplot as plt
import warnings
import sys


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


def main():
    # Test for the issue with UserWarning when all values are "bad" (np.nan)
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter("always")
        plt.scatter(np.ones(10), np.ones(10), c=np.full(10, np.nan))
        plt.show()
        # Expecting UserWarning to be present
        assert any(isinstance(warning.message, UserWarning) for warning in w), "Issue 1: Warning not raised for all NaN values."

    # Test for the issue with StopIteration when yerr contains only NaN values
    try:
        fig, ax = plt.subplots(1, 1)
        ax.errorbar([0], [0], yerr=[np.nan])  # This should not raise StopIteration
    except Exception as e:
        print_stacktrace(e)
        assert False, "Issue 2: Exception raised for all NaN values in yerr."

    print("Both issues reproduced successfully (assuming correct AssertionError).")


if __name__ == "__main__":
    main()
