import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def test_datetime_units_in_bar():
    try:
        fig, ax = plt.subplots()
        start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
        stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])
        # Attempt to plot without specifying datetime handling
        rects = ax.barh([0, 1, 3], width=stop-start, left=start)
        
        # Check if the axis have been automatically recognized as datetime
        if not isinstance(ax.xaxis.converter, mdates.DateConverter):
            raise AssertionError("Datetime units were not automatically recognized in barh 'left' parameter.")
        
        # Repeating the check for ax.bar which uses the 'bottom' parameter
        fig, ax = plt.subplots()
        rects = ax.bar([0, 1, 3], height=stop-start, bottom=start)
        
        if not isinstance(ax.yaxis.converter, mdates.DateConverter):
            raise AssertionError("Datetime units were not automatically recognized in bar 'bottom' parameter.")

    except Exception as e:
        print_stacktrace(e)
        exit(1) # Exit with error since the test did not pass
    print("Test passed: Datetime units were correctly interpreted.")
    exit(0) # Exit without error, indicating success

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
    test_datetime_units_in_bar()
