import matplotlib.pyplot as plt
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

fig = plt.figure()
subfigs = fig.subfigures(2, 1)
axarr = subfigs[0].subplots(2, 2)

try:
    plt.sca(axarr[0, 0])
    raise AssertionError("Issue is not present")
except TypeError as e:
    print_stacktrace(e)
    sys.exit(1)
