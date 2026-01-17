import numpy as np
from scipy import signal
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

def test_windows_correction():
    window = signal.windows.flattop(512)
    actual = (np.abs(window).sum()**2-window.sum()**2)
    expected = 0
    if actual != expected:
        raise AssertionError(f"Expected {expected} but got {actual}")

if __name__ == "__main__":
    try:
        test_windows_correction()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
