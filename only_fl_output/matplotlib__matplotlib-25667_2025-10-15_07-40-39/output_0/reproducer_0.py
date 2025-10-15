import numpy as np
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

def main():
    try:
        # Attempt to reproduce the issue
        fig, ax = plt.subplots()
        start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
        stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])
        bars = ax.barh([0, 1, 3], width=stop-start, left=start)

        # This part is to check if the left parameter (start dates) triggers datetime units properly
        # We measure this by inspecting the type of the first tick on x-axis
        # If the issue is present, the type won't be matplotlib.dates.DateFormatter
        # indicating the datetime units were not triggered correctly
        fig.canvas.draw()  # Required to ensure ticks have been drawn
        xaxis_formatter = ax.xaxis.get_major_formatter()
        assert isinstance(xaxis_formatter, plt.matplotlib.dates.DateFormatter), "Datetime units not triggered for barh"

        print("Issue not reproduced. Datetime units are triggered correctly for barh.")

    except AssertionError as e:
        print_stacktrace(e)
        return 1  # Return non-zero to indicate the presence of the issue

    return 0  # Return zero to indicate the issue is not present

if __name__ == "__main__":
    import sys
    sys.exit(main())
