# reproducer.py
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
    import xarray as xr

    try:
        # Load the example dataset
        ds = xr.tutorial.load_dataset("air_temperature")
        # Apply the xr.where function as described in the issue
        result_attrs = xr.where(True, ds.air, ds.air, keep_attrs=True).time.attrs
        # Expected time attributes before the issue
        expected_attrs = {'standard_name': 'time', 'long_name': 'Time'}
        
        # Check if the issue is present. Assert will raise an AssertionError if the check fails.
        assert result_attrs == expected_attrs, "Coordinate attributes are overwritten by variable attributes."
    
    except AssertionError as e:
        print_stacktrace(e)
        raise

    except Exception as e:
        print("An unexpected error occurred.", file=sys.stderr)
        print_stacktrace(e)
        sys.exit(1)

    else:
        print("Success: The issue is resolved.")
        sys.exit(0)

if __name__ == "__main__":
    main()
