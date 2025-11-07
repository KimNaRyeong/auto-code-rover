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
    import numpy as np
    import matplotlib.pyplot as plt

    try:
        # Create figure and axes
        fig, ax = plt.subplots()

        # Define start and stop dates
        start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
        stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])

        # Plot using `barh` and `bar` to replicate the issue
        ax.barh([0, 1, 3], width=stop-start, left=start)
        
        # --------------------------------------------------------------------------------
        # Expected: Check if Matplotlib correctly handles the conversion of datetime units
        # Let's check the axis type to confirm if it's a datetime axis as expected.
        xaxis_type = ax.xaxis.converter
        expected_axis_type = plt.matplotlib.dates.DateConverter
        if xaxis_type is not expected_axis_type:
            raise AssertionError("Datetime conversion for x-axis not triggered by `barh`.")

        # Reset plot and now check for `bar` with datetime conversion
        fig, ax = plt.subplots()
        ax.bar([0, 1, 3], height=stop-start, bottom=start)
        yaxis_type = ax.yaxis.converter
        if yaxis_type is not expected_axis_type:
            raise AssertionError("Datetime conversion for y-axis not triggered by `bar`.")

        print("Datetime units handling works as expected with `bar` and `barh`.")

    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
