import matplotlib.pyplot as plt
from io import StringIO
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

try:
    import matplotlib.pyplot as plt
    the_rc = plt.style.library["seaborn-colorblind"]
except KeyError as e:
    print_stacktrace(e)
    raise AssertionError("Issue reproduced")
else:
    print("Issue not reproduced")
    sys.exit(0)
