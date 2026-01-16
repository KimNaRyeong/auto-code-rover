To create a standalone `reproducer.py` file that properly tests for the issue described, we need to account not only for the scenarios presented but also ensure environmental readiness (e.g., the presence of Matplotlib). Given the error encountered, it appears there was an attempt to run the script in an environment where Matplotlib was not installed. 

For someone running this script, they should make sure that Matplotlib is installed. However, the script itself will not manage environment setup—it's expected that the necessary libraries are installed beforehand. 

Here's an adjusted version of `reproducer.py` focusing on raising an `AssertionError` if the issue is present, which also integrates the specified function to print the stack trace clearly when exceptions related to the issue are caught.

```python
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

def test_scatter():
    # This part tests the first "working" cases.
    try:
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((3, 4)))
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((4, 3)))
    except Exception as e:
        print("Unexpected exception for case that should work:", e)
        print_stacktrace(e)
        assert False, "Unexpected exception occurred for valid inputs."
    
    # This tests the failing cases and checks that a ValueError is raised.
    for c_shape in [(6, 2), (12,)]:
        try:
            plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape(c_shape))
            assert False, f"Expected ValueError for shape {c_shape} not raised."
        except ValueError as e:
            pass # This is expected.
        except Exception as e:
            print(f"Unexpected exception type for c shape {c_shape}: {e.__class__.__name__}")
            print_stacktrace(e)
            assert False, f"Unexpected exception type for c shape {c_shape}."

if __name__ == "__main__":
    test_scatter()
    print("Test completed - if no AssertionError was raised, the issue might be resolved.")
```

Please execute this script in an environment where Matplotlib is installed. If Matplotlib is not installed, you can install it via pip with the command `pip install matplotlib`. 

This script now includes:
- Two tests that should work according to the initial problem description, not expecting any exceptions for them.
- Tests that execute scenarios known to fail due to shape mismatches, expecting `ValueError` to be raised. 

It exits with code 0 if all assertions pass, indicating the issue may be resolved or not present. Any caught exceptions related to the bug will trigger an `AssertionError`, with the script outputting a formatted stack trace for clarity.