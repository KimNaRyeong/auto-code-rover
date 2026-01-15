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

def test_cftime_range_with_milliseconds():
    try:
        result = xr.cftime_range("2000-01-01", periods=3, freq='10L')
        expected_output = ["2000-01-01 00:00:00", "2000-01-01 00:00:00.010000", "2000-01-01 00:00:00.020000"]
        # Convert CFTimeIndex to string for comparison since we expect an exact match with expected_output
        result_formatted = [str(date) for date in result]
        assert result_formatted == expected_output, "CFTime range did not match the expected output for milliseconds."
        print("Test Passed: CFTime range matches the expected output for milliseconds.")
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Test Failed: CFTime range did not support millisecond frequency.")

def test_cftime_range_with_microseconds():
    try:
        result = xr.cftime_range("2000-01-01", periods=3, freq='1U')
        expected_output = ["2000-01-01 00:00:00", "2000-01-01 00:00:00.000001", "2000-01-01 00:00:00.000002"]
        # Convert CFTimeIndex to string for comparison since we expect an exact match with expected_output
        result_formatted = [str(date) for date in result]
        assert result_formatted == expected_output, "CFTime range did not match the expected output for microseconds."
        print("Test Passed: CFTime range matches the expected output for microseconds.")
    except ValueError as e:
        print_stacktrace(e)
        raise AssertionError("Test Failed: CFTime range did not support microsecond frequency.")

if __name__ == "__main__":
    test_cftime_range_with_milliseconds()
    test_cftime_range_with_microseconds()
```