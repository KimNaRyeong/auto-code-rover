# Attempt to import matplotlib, install if unavailable
try:
    import matplotlib.pyplot as plt
except ImportError:
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "matplotlib"])
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

def test_scatter_c_shape_handling():
    try:
        # These calls should work based on the way matplotlib handles shapes
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((3, 4)))
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((4, 3)))
        
        # Raises error due to shape mismatch
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12).reshape((6, 2)))
        print_stacktrace(ValueError("The shape of `c` did not cause a failure as expected."))
        
        # Raises error due to flat array with otherwise matching size
        plt.scatter(np.arange(12).reshape((3, 4)), np.arange(12).reshape((4, 3)), c=np.arange(12))
        print_stacktrace(ValueError("The flat `c` array did not cause a failure as expected."))
        
    except ValueError as e:
        print_stacktrace(e)
        if "argument has 12 elements, which is not acceptable for use with 'x' with size 12, 'y' with size 12" in str(e):
            # This is the expected failure mode for the last test
            return
        else:
            # This is unexpected; re-raise the exception for visibility
            raise
    except Exception as e:
        # This means there was unexpected failure; we print the stacktrace and re-raise.
        print_stacktrace(e)
        raise
    
    # If we reach this point without exceptions, the issue is incorrectly considered fixed.
    raise AssertionError("The issue with inconsistent shape handling of parameter `c` in `scatter` was not reproduced.")

if __name__ == "__main__":
    test_scatter_c_shape_handling()
    print("Test completed. If no AssertionError was raised, the issue is considered fixed.")
