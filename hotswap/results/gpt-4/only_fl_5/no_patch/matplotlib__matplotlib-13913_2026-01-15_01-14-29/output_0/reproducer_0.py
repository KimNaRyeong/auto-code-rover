# reproducer.py

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

def test_color_like_issue():
    import matplotlib
    import matplotlib.pyplot as plt
    import numpy as np

    c = np.arange(1000).astype(str)
    X = np.random.normal(0, 1, [1000, 2])

    try:
        assert all([matplotlib.colors.is_color_like(color) for color in c])
        plt.scatter(X[:, 0], X[:, 1], c=c)
        # If it gets here without an exception, then the issue is considered fixed, exit with code 0.
        print("Issue Fixed. Exiting with code 0.")
        exit(0)
    except AssertionError as ae:
        # This is for an assertion failure, which we don't expect to happen.
        print_stacktrace(ae)
        exit(1)
    except Exception as e:
        # Here we catch the ValueError that is the root cause of our issue
        # If this exception is caught, it proves the issue still exists.
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    test_color_like_issue()
