import math
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

try:
    f = StringIO()
    with redirect_stdout(f):
        print(math.pi ** (1/math.e))
    output = f.getvalue().strip()
    if not output.startswith("π"):
        raise AssertionError("Inaccurate rendering of pi**(1/E)")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully. Exiting with code 0.")
exit(0)
