import numpy as np
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
    window = np.array([1.0, -0.5, 0.0, -0.5, 1.0])
    actual = (np.abs(window).sum()**2-window.sum()**2)
    expected = 0
    assert actual == expected, f"Expected {expected}, but got {actual}"

if __name__ == "__main__":
    try:
        test_windows_correction()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
