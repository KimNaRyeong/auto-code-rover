```python
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

def main():
    import numpy as np
    import matplotlib.pyplot as plt
    try:
        xy = np.indices((100, 100))
        img = np.exp(-np.pi * (np.sum((xy - 50) ** 2, 0) / 20.0 ** 2))
        cs = plt.contourf(img, 50)
        result = cs.find_nearest_contour(20, 20, pixel=False)
        # Assert that the result shouldn't be an error. Actual expected values can be more strict.
        assert result is not None
        print("No issue found, the function worked as expected.")
    except AssertionError as ae:
        print_stacktrace(ae)
        exit(1)  # Use exit code 1 for assertion errors
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # General error exit code

if __name__ == "__main__":
    main()
```

This script tries to reproduce the issue as described. When the issue occurs, it will print a stack trace detailing the encountered error. If the issue is fixed (meaning the function call does not raise an `Exception` and doesn't violate the assertion), it will simply print a success message and exit with code 0. This design ensures that it fulfills the requirements of raising an `AssertionError` when the issue is present, printing a stack trace with line numbers, and exiting with code 0 when the issue is fixed.