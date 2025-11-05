import matplotlib.pyplot as plt
import sys
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

def test_issue():
    f, a = plt.subplots()
    l, = a.plot([1, 2])
    l.remove()
    assert not hasattr(l, 'axes')

    f, a = plt.subplots()
    l, = a.plot([1, 2])
    a.cla()
    if hasattr(l, 'axes'):
        raise AssertionError("cla() and clf() should unset the .axes attribute of deparented artists")

try:
    test_issue()
except AssertionError as e:
    print_stacktrace(e)
    sys.exit(1)

sys.exit(0)
