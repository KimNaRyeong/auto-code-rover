Based on your requirements, here's how you could structure the `reproducer.py` script to specifically target reproducing the issue related to CFTime offsets missing for millisecond and microsecond frequencies. This script checks for the expected failure when attempting to create a CFTime range with millisecond ('L') frequency, catching and examining the `ValueError`. If the error message matches what's expected, it indicates the issue is present. If the operation succeeds in the future, implying the issue has been resolved, it will print a success message and exit with code 0.

Please note, running this script requires an environment where `xarray` and its dependencies are correctly installed and compatible with such datetime operations.

```python
# reproducer.py
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

try:
    # Attempt to create a CFTime range with a millisecond offset
    result = xr.cftime_range("2000-01-01", periods=3, freq='10L')
    expected_first_element = '2000-01-01 00:00:00.010000'
    assert result[1].isoformat() == expected_first_element, "The output does not match the expected millisecond precision."
    print("Successfully generated a CFTime range with millisecond precision. Issue seems to be resolved.")
except ValueError as e:
    print_stacktrace(e)
    assert "Invalid frequency string provided" in str(e), "Unexpected error message"
    exit(1)  # Exit with an error code indicating failure to resolve the expected behavior.
except Exception as e:
    print_stacktrace(e)
    print("An unexpected error occurred, which might indicate a different issue.")
    exit(1)
else:
    exit(0)  # Exit successfully if no exception was raised, indicating the issue may be resolved.
```

This file should be placed in the root directory of the project and executed with Python 3. If the script exits with code 1, it has successfully reproduced the issue as per the instructions. Should future developments in `xarray` address this matter, enabling millisecond and microsecond precision in `cftime_range`, the script is designed to exit gracefully with code 0, signaling the issue's resolution.