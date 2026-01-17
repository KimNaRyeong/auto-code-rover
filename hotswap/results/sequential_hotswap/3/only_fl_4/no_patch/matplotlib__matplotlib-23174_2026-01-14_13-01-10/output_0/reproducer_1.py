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
    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-(X**2) - Y**2)
    Z2 = np.exp(-((X - 1) ** 2) - (Y - 1) ** 2)
    Z = (Z1 - Z2) * 2

    fig = plt.figure()
    # Adjusting the script slightly to be more explicit in its expectation of failure.
    try:
        figs = fig.subfigures(nrows=1, ncols=2)

        for f in figs:
            ax = f.subplots()
            CS = ax.contour(X, Y, Z)
            ax.clabel(CS, inline=True, fontsize=10)
            ax.set_title("Simplest default with labels")
        plt.show()
        # Raising an AssertionError directly here to indicate issue presence expected
        raise AssertionError("Expected issue not encountered")

    except AttributeError as e:
        print_stacktrace(e)
        print("Issue reproduced successfully, as expected.")
        # Exiting gracefully here indicates successful reproduction of the bug.
        exit(0)
    except Exception as ex:
        print("An unexpected error occurred, not related to the original issue. Error details:")
        print_stacktrace(ex)
        raise

if __name__ == "__main__":
    main()
