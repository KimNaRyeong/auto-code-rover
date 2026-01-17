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
        ds = xr.tutorial.load_dataset("air_temperature")
        result_attrs = xr.where(True, ds.air, ds.air, keep_attrs=True).time.attrs

        # Expected time attributes not to be overwritten by variable attributes
        expected_attrs = {'standard_name': 'time', 'long_name': 'Time'}
        assert expected_attrs.items() <= result_attrs.items(), "Coordinate attributes were overwritten."

    except Exception as e:
        print_stacktrace(e)
        raise

    print("Test passed, issue is not present.")


if __name__ == "__main__":
    main()
