import matplotlib.pyplot as plt
import sys
from traceback import extract_tb, print_exception

def print_stacktrace(e: Exception):
    print("Traceback (most recent call last):", file=sys.stderr)
    tb = extract_tb(e.__traceback__)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    try:
        f, a = plt.subplots()
        l, = a.plot([1, 2])
        l.remove()
        if l.axes is not None:
            raise AssertionError("Expected l.axes to be None")
        a.cla()
        if l.axes is None:
            raise AssertionError("Expected l.axes to be set after cla()")
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    reproduce_issue()
