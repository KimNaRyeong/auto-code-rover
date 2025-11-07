import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_barh_issue():
    fig, ax = plt.subplots()
    start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
    stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])
    ax.barh([0, 1, 3], width=stop-start, left=start)
    plt.draw()
    assert isinstance(ax.xaxis.converter, mdates.DateConverter), "barh did not trigger datetime units"
    print("Issue not present")

def test_bar_issue():
    fig, ax = plt.subplots()
    start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
    stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])
    ax.bar([0, 1, 3], height=stop-start, bottom=start)
    plt.draw()
    assert isinstance(ax.yaxis.converter, mdates.DateConverter), "bar did not trigger datetime units"
    print("Issue not present")

try:
    test_barh_issue()
    test_bar_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
