"""reproducer.py - Reproduces the misleading exception in TimeSeries when a required column is removed."""

def reproduce_issue():
    from astropy.time import Time
    from astropy.timeseries import TimeSeries
    import numpy as np

    time = Time(np.arange(100000, 100003), format='jd')
    ts = TimeSeries(time=time, data={"flux": [99.9, 99.8, 99.7]})
    # Explicitly setting required columns for reproduction; not a typical usage scenario.
    ts._required_columns = ["time", "flux"]
    ts.remove_column("flux")

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = f"'{frame.line.strip()}'" if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    Line {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        reproduce_issue()
        print("Issue not reproduced. Exiting with code 0.")
    except Exception as e:
        print_stacktrace(e)
        expected_message = "TimeSeries object is invalid - expected 'time' as the first columns but found 'time'"
        assert str(e) == expected_message, "Unexpected exception message"
        print("Issue reproduced successfully. AssertionError was raised due to the present issue.")

if __name__ == "__main__":
    main()
