import matplotlib.pyplot as plt
import traceback
import sys

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
    f, a = plt.subplots()
    l, = a.plot([1, 2])
    l.remove()
    assert not hasattr(l, 'axes')
    
    f, a = plt.subplots()
    l, = a.plot([1, 2])
    a.cla()
    if hasattr(l, 'axes'):
        raise AssertionError("cla() should unset the `.axes` attribute of deparented artists")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Test passed.")
exit(0)
