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


def test_find_nearest_contour():
    import numpy as np
    import matplotlib.pyplot as plt

    xy = np.indices((100, 100))
    img = np.exp(-np.pi * (np.sum((xy - 50) ** 2, 0) / 20. ** 2))
    cs = plt.contourf(img, 50)

    try:
        result = cs.find_nearest_contour(20, 20, pixel=False)
        # Assuming the expected outcome tuple length from the bug description
        assert len(result) == 6, "find_nearest_contour result does not match expected outcome."
        print("Issue is fixed.")
    except Exception as e:
        print_stacktrace(e)
        # An AssertionError is raised when our explicit check fails.
        # Other exceptions are caught by the general exception handler above.
        raise AssertionError("Issue with find_nearest_contour is present.") from e


if __name__ == "__main__":
    test_find_nearest_contour()
