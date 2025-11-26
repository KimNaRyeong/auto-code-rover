import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

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
    fig, ax = plt.subplots()
    start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
    stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])

    ax.barh([0, 1, 3], width=stop-start, left=start)

    # Check if the x-axis is a date axis
    locator = mdates.AutoDateLocator()
    formatter = mdates.ConciseDateFormatter(locator)
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    fig.autofmt_xdate()

    plt.draw()
    plt.savefig('barhtime.png')

    # Check if the plot is correct
    with open('barhtime.png', 'rb') as f:
        image_data = f.read()
    expected_image_data = ...  # Replace with the expected image data

    if image_data != expected_image_data:
        raise AssertionError("bar/h doesn't trigger datetime units")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        exit(1)

exit(0)
