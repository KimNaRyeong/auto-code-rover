#!/usr/bin/env python3
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
    import matplotlib.pyplot as plt
    import numpy as np

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
        # If no exception is raised, assertion fails.
        raise AssertionError("Issue not present. savefig with .jpg and metadata did not fail as expected.")
    except TypeError as e:
        if "metadata" in str(e) and "unexpected keyword argument" in str(e):
            print("Issue is present as expected. Raising AssertionError.")
            print_stacktrace(e)
        else:
            print("Unexpected TypeError encountered.")
            print_stacktrace(e)
            raise AssertionError("Unexpected error. Issue might have changed.")
    except Exception as e:
        print("An unexpected exception occurred:")
        print_stacktrace(e)
        raise AssertionError("Unexpected exception. Issue might have changed.")

if __name__ == "__main__":
    main()
