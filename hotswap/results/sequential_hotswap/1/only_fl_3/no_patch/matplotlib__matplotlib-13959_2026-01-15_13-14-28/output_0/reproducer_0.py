import numpy as np
import matplotlib.pyplot as plt

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

def test_inconsistent_shape_handling():
    try:
        # Case 1: Implicit ravel() works.
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((3, 4)))
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((4, 3)))

        # Case 2: Different shape but same size fails.
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((6, 2)))
        assert False, "Case 2 failed to raise ValueError"

    except ValueError as e:
        error_message = str(e)
        if "which is not acceptable for use with 'x' with size 12, 'y' with size 12" not in error_message:
            print_stacktrace(e)
            assert False, "Unexpected error message"

    try:
        # Case 3: Using 1D array for c fails.
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12))
        assert False, "Case 3 failed to raise ValueError"

    except ValueError as e:
        error_message = str(e)
        if "which is not acceptable for use with 'x' with size 12, 'y' with size 12" not in error_message:
            print_stacktrace(e)
            assert False, "Unexpected error message in Case 3"

if __name__ == "__main__":
    test_inconsistent_shape_handling()
    print("If no error is raised, the issue is fixed.")
