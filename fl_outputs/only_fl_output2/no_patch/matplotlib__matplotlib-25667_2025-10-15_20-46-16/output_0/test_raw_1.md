```python
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

def check_for_issue():
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.dates import date2num

    fig, ax = plt.subplots()

    start = np.array([np.datetime64('2012-01-01'), np.datetime64('2012-02-01'), np.datetime64('2012-01-15')])
    stop = np.array([np.datetime64('2012-02-07'), np.datetime64('2012-02-13'), np.datetime64('2012-02-12')])
    
    # Calculate the width by converting to matplotlib dates
    widths = date2num(stop) - date2num(start)
    
    # Attempting to reproduce the issue with barh
    rects = ax.barh([0, 1, 3], width=widths, left=date2num(start))

    if not all(rect.get_width() > 0 for rect in rects):
        raise AssertionError("barh doesn't trigger datetime units correctly.")

    # Clear the figure for a second attempt with bar
    ax.clear()

    # Attempting to reproduce the issue with bar
    rects = ax.bar([0, 1, 3], height=widths, bottom=date2num(start))

    if not all(rect.get_height() > 0 for rect in rects):
        raise AssertionError("bar doesn't trigger datetime units correctly.")

    # If no exceptions were raised, the issue is fixed
    print("Issue is fixed.")

if __name__ == "__main__":
    try:
        check_for_issue()
    except AssertionError as e:
        print_stacktrace(e)
        print("Issue reproduced. Exiting with code 1.")
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        print("Unexpected error. Exiting with code 1.")
        exit(1)
    else:
        # Exiting with code 0 if no issue is detected
        exit(0)
```

This `reproducer.py` is designed to check whether the issue with `bar` and `barh` not triggering datetime units in Matplotlib is present. If the conditions indicative of the issue are met (e.g., the width or height of bars being incorrect), an `AssertionError` is raised, and the script prints a detailed stack trace. The script exits with code 1 if the issue is present, indicating failure, and exits with code 0 if the issue is not detected, indicating success.