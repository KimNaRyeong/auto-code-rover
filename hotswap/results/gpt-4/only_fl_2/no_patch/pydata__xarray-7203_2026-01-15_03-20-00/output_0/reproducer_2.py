# reproducer.py
import time
from unittest.mock import patch
import xarray as xr

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

def mock_repr_html_(*args, **kwargs):
    """
    Mocked _repr_html_ to simulate a long-running process for loading
    multiple small variables in repr. This function will just sleep for 2 seconds.
    """
    time.sleep(2) # Simulate the processing time
    return "<b>Mocked Representation</b>"

def main():
    try:
        # Patching the _repr_html_ method in xarray.Dataset with our mock to simulate slow loading
        with patch('xarray.core.dataset.Dataset._repr_html_', side_effect=mock_repr_html_):
            start_time = time.time()
            ds = xr.Dataset() # Normally you'd load or create a dataset
            _ = ds._repr_html_()  # Trigger mocked dataset representation
            end_time = time.time()
            duration = end_time - start_time
            print(f"Representation Time: {duration}s")
            assert duration < 1, "The dataset representation took too long."

    except AssertionError as e:
        print_stacktrace(e)
        exit(1)  # Exit with code 1 to indicate failure due to assertion error
    except Exception as e:
        print_stacktrace(e)
        exit(1)  # General failure
    else:
        print("Test passed successfully.")
        exit(0)  # Exit with code 0 to indicate success

if __name__ == "__main__":
    main()
