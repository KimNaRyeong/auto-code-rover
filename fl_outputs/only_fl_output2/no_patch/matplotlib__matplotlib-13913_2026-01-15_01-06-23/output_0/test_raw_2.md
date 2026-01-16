```python
# reproducer.py

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        c = np.arange(1000).astype(str)
        X = np.random.normal(0, 1, [1000, 2])

        # Make an assertion to check the bug's condition
        assert not all([matplotlib.colors.is_color_like(color) for color in c]), "is_color_like returns True for strings of integers."
        print("Assertion passed, issue not found, exiting with code 0.")
        sys.exit(0)
    except AssertionError as e:
        print(e)
        sys.exit(0)  # Exiting with code 0 as instructed for reproduction failure
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)  # Exiting with code 1 to indicate an unexpected error occurred

if __name__ == '__main__':
    main()
```

This script specifically tests for the bug where `matplotlib.colors.is_color_like` is erroneously returning `True` for strings that are representations of integers, which should not be recognized as valid color inputs. The assertion is expected to fail when the bug is present, as the condition being asserted is that not all strings of integers should pass the `is_color_like` check.

If the assertion fails (i.e., an `AssertionError` is raised), it means the bug is successfully reproduced, and the script prints the error message and exits with code 0, indicating deliberate failure as per the instruction for bug presence.

For any other kinds of exceptions that are not `AssertionError`, the script prints a detailed stack trace to help in debugging the issue further and exits with code 1, indicating an unexpected error during the test execution.