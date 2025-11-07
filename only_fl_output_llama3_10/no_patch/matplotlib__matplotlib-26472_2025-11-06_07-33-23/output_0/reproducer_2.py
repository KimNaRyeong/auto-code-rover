import matplotlib.pyplot as plt
from io import StringIO
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
    try:
        with plt.rc_context():
            plt.switch_backend('qt5')
            plt.ioff()
            plt.plot([1, 3, 2])
            plt.show(block=True)
            plt.ion()
            plt.switch_backend('inline')
    except Exception as e:
        raise AssertionError("Issue reproduced") from e

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
