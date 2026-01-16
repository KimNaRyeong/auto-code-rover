# reproducer.py
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

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

def test_is_color_like_with_integer_strings():
    c = np.arange(1000).astype(str)
    X = np.random.normal(0, 1, [1000, 2])

    try:
        assert all([matplotlib.colors.is_color_like(color) for color in c]), "Invalid color representation detected."
        plt.scatter(X[:, 0], X[:, 1], c=c)
        print("No issue detected. The bug might have been fixed.")
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print("An error occurred which is likely related to the reported bug.")
        print_stacktrace(e)
        sys.exit(1)

if __name__ == "__main__":
    test_is_color_like_with_integer_strings()
