Below is a standalone python script named `reproducer.py`. This script is written to reproduce the reported issue with `tripcolor` ignoring the `clim` parameter. It will attempt to verify if the color mapping correctly applies the `clim` range as expected. If the issue is present (i.e., the `clim` parameter is ignored), it will raise an `AssertionError` and print a detailed stack trace. Otherwise, if the issue is resolved and the behavior is as expected, the script will exit normally with code 0.

```python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib

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

def test_tripcolor_clim():
    x = np.random.rand(100)
    y = np.random.rand(100)
    z = np.random.rand(100)
    fig, ax = plt.subplots()
    collection = ax.tripcolor(x, y, z, clim=(0, 0.5))
    plt.colorbar(collection)

    # Get the limits of the color mapping
    clim_actual = collection.get_clim()

    # Expected clim values
    clim_expected = (0, 0.5)

    try:
        assert clim_actual == clim_expected, f"clim_actual {clim_actual} != clim_expected {clim_expected}"
    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    test_tripcolor_clim()

    # If no exception was raised, the test passed
    print("Test passed successfully.")
```

This script performs the following steps:

1. Uses `matplotlib` to plot random data using `tripcolor`, specifying the color limit (`clim`) explicitly.
2. Retrieves the actual color limit (`clim`) used by the `tripcolor` plot.
3. Asserts whether the actual `clim` matches the expected `clim` values. If they do not match (indicating that the `clim` parameter was ignored), it raises an `AssertionError`.
4. If an AssertionError is caught, it uses the `print_stacktrace` function to print the stack trace and then re-raises the exception to halt execution.
5. If the script executes without raising an `AssertionError`, it indicates the test passed successfully, printing a confirmation message.

To run this test, place `reproducer.py` in the root directory of your project and execute it using Python 3:

```
python3 reproducer.py
```

Ensure you have the specified version of Matplotlib installed, or adjust the script accordingly for compatibility with the version you are testing with.