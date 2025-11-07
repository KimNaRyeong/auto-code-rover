import matplotlib.pyplot as plt
from io import StringIO
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

def reproduce_bug():
    try:
        import matplotlib.pyplot as plt
        fig = plt.figure()
        subfigs = fig.subfigures(2, 1)
        axarr = subfigs[0].subplots(2, 2)
        plt.sca(axarr[0, 0])
        assert False, "Issue not reproduced"
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue reproduced")

if __name__ == "__main__":
    reproduce_bug()
