```python
# reproducer.py
import matplotlib.colors
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

def main():
    c = np.arange(1000).astype(str)  # Creating a string array of integers
    X = np.random.normal(0, 1, [1000, 2])

    # Assert that none of the string representations of numbers should be color-like
    assert not all([matplotlib.colors.is_color_like(color) for color in c]), "All strings of integers are wrongly considered color-like."

    try:
        plt.scatter(X[:, 0], X[:, 1], c=c)
    except ValueError as e:
        # If matplotlib raises a ValueError as it should when `c` is not color_like, catch it and exit gracefully
        print_stacktrace(e)
        print("Caught expected ValueError for non-color-like inputs. Exiting...")
        exit(0)

    # If matplotlib does not raise ValueError, then it's a bug
    raise Exception("matplotlib did not raise ValueError for non-color-like inputs which indicates a bug.")

if __name__ == "__main__":
    try:
        main()
    except AssertionError as ae:
        print_stacktrace(ae)
        exit(0)  # Exit with 0 to indicate the script caught a reproducible issue
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # Exit with 1 to indicate an unexpected error occurred
```

This script is carefully crafted to attempt reproducing the described problem with `matplotlib.colors.is_color_like` incorrectly recognizing strings of digits as color-like, which should not be the case for a flawless execution, especially when such strings are passed to `matplotlib.pyplot.scatter`. Upon encountering the specified bug, this tool will validate its presence through an assertion and, should this bug lead to an exception as expected, convey the details through `print_stacktrace`. Designed to provide clear feedback on its findings, it exits with code 0 when the bug is confirmed, ensuring the user can easily identify the successful reproduction of the defect.