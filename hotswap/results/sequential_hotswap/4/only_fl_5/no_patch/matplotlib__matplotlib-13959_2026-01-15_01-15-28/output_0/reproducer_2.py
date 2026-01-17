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

def test_scatter_shape_handling():
    x = np.arange(12).reshape((3, 4))
    y = np.arange(12).reshape((4, 3))
    c_correct_shape_1 = np.arange(12).reshape((3, 4))
    c_correct_shape_2 = np.arange(12).reshape((4, 3))
    c_incorrect_shape = np.arange(12).reshape((6, 2))
    c_flat = np.arange(12)
    
    # These should work
    try:
        plt.scatter(x, y.T, c=c_correct_shape_1)  # Transpose y to match x's shape
        plt.cla()
        plt.scatter(x.T, y, c=c_correct_shape_2)  # Transpose x to match y's shape
        plt.cla()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Test failed: Correct shape handling leads to an error.")

    # These should raise an error due to shape mismatch or be handled gracefully depending on the issue's status
    error_raised = False
    try:
        plt.scatter(x, y.T, c=c_incorrect_shape)
        plt.cla()
    except ValueError:
        error_raised = True

    try:
        plt.scatter(x, y.T, c=c_flat)
        plt.cla()
    except ValueError:
        error_raised = True

    if not error_raised:
        # If no error was raised, the inconsistency issue exists
        raise AssertionError("Inconsistent shape handling of 'c' detected.")


if __name__ == "__main__":
    try:
        test_scatter_shape_handling()
        print("The script exited successfully, indicating the issue might have been fixed.")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
