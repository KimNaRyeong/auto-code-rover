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

try:
    import numpy as np
    from matplotlib import pylab as plt
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')
    ax.scatter([1, np.nan, 3], [2, np.nan, 4], [3, np.nan, 5], color=[[.5, .5, .5, .5]]*3, s=11.5)
    plt.show()
    # If the execution reaches this point without error, AssertionError is raised
    raise AssertionError("Issue not present, 'scatter' handled NaN values as expected.")
except ValueError as e:
    print_stacktrace(e)
    exit(0)  # Exit with 0 to indicate the script executed successfully, even if it identified the issue.
