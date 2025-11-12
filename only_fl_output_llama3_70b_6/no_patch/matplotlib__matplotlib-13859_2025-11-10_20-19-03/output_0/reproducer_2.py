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

try:
    plt.subplots(1, 1, figsize=(3, 0))
    plt.savefig("test.png")
except (RuntimeError, AttributeError, SystemError) as e:
    if "tile cannot extend outside image" in str(e):
        print_stacktrace(e)
        raise AssertionError("Zero-width figure crashes libpng") from e
    else:
        print_stacktrace(e)
        sys.exit(1)

sys.exit(0)
