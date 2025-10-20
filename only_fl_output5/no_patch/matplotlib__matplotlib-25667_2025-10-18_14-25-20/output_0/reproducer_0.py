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


def check_barh_with_datetime():
    fig, ax = plt.subplots()
    start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
    stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])
    ax.barh([0, 1, 3], width=stop-start, left=start)
    ax.set_xlim([np.datetime64('2012-01-01'), np.datetime64('2012-03-01')])  # Set limits to ensure datetime x-axis
    xaxis_type = type(ax.xaxis.converter)
    expected = 'DatetimeConverter'
    assert xaxis_type.__name__ == expected, f"Expected xaxis converter type to be {expected}, got {xaxis_type.__name__}"


def main():
    try:
        check_barh_with_datetime()
        print("The issue is not present.")
    except AssertionError as e:
        print_stacktrace(e)
        raise


if __name__ == '__main__':
    main()
