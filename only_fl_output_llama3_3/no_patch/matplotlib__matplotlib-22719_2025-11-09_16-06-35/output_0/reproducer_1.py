import matplotlib.pyplot as plt
import sys
import traceback

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

def reproduce_issue():
    f, ax = plt.subplots()
    ax.xaxis.update_units(["a", "b"])
    try:
        ax.plot([], [])
        assert False, "Issue not reproduced"
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

reproduce_issue()
