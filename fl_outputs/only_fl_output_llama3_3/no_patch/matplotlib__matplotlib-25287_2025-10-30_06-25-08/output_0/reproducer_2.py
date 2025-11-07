import matplotlib.pyplot as plt
from io import StringIO
from contextlib import redirect_stdout

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
    try:
        plt.rcParams.update({'ytick.labelcolor': 'red'})
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.plot([1.01e9,1.02e9,1.03e9])
        offset_text = ax.yaxis.offsetText
        assert offset_text.get_color() == 'black'
    except AssertionError as e:
        f = StringIO()
        with redirect_stdout(f):
            print_stacktrace(e)
        print(f.read(), file=sys.stderr)
        sys.exit(1)

reproduce_issue()
