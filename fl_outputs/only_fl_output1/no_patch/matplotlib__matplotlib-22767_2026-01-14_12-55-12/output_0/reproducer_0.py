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

    # Data setup
    xy = np.indices((100, 100))
    img = np.exp(-np.pi * (np.sum((xy - 50) ** 2, 0) / 20. ** 2))

    # Contour setup
    cs = plt.contourf(img, 50)

    # Test find_nearest_contour method
    try:
        result = cs.find_nearest_contour(20, 20, pixel=False)
        print(result)  # If no exception, print the result
    except Exception as e:
        print_stacktrace(e)  # Print the stack trace if there's an error
        raise AssertionError("The expected issue occurred.")

if __name__ == "__main__":
    test_find_nearest_contour()
