#!/usr/bin/env python3
import matplotlib.pyplot as plt
import numpy as np


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


def main():
    plt.style.use('_mpl-gallery')

    # make data
    x = np.linspace(0, 10, 100)
    y = 4 + 2 * np.sin(2 * x)

    # plot
    fig, ax = plt.subplots()

    ax.plot(x, y, linewidth=2.0)

    ax.set(xlim=(0, 8), xticks=np.arange(1, 8),
           ylim=(0, 8), yticks=np.arange(1, 8))

    try:
        plt.savefig("sin.jpg", metadata={})
        print("Error: The issue is not present. The savefig operation completed without raising an exception.")
    except TypeError as e:
        # Checks if the TypeError is specifically about the unexpected 'metadata' keyword
        if "unexpected keyword argument 'metadata'" in str(e):
            print_stacktrace(e)
        else:
            raise AssertionError("The error raised is not the expected 'unexpected keyword argument' error.")

    except Exception as e:
        print("An unexpected error occurred:")
        print_stacktrace(e)
        raise AssertionError("An unexpected exception occurred.")


if __name__ == "__main__":
    main()
