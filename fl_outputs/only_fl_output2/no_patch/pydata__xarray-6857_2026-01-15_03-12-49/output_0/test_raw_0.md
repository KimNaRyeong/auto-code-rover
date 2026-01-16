```python
# reproducer.py
def main():
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

    da_withunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
    da_withunits.frequency.attrs["units"] = "GHz"
    initial_units = da_withunits.frequency.attrs.get("units", "")
    
    da_withoutunits = xr.DataArray([1, 1, 1], coords={"frequency": [1, 2, 3]})
    
    # Perform the equality check that's causing the issue
    try:
        print(da_withunits == da_withoutunits)  # This is expected to work without side effects
        
        # Verify that the attributes are unchanged
        final_units = da_withunits.frequency.attrs.get("units", "")
        assert initial_units == final_units, "The units attribute should not have changed."
    
    except Exception as e:
        print_stacktrace(e)
    
    else:
        print("Test passed: attributes are unchanged after comparison.")
        # Exiting with code 0 as requested for when the issue is fixed
        import sys
        sys.exit(0)

if __name__ == "__main__":
    main()
```

This Python script will attempt to reproduce the issue described, which is the unexpected modification of a `DataArray`'s attributes when comparing two `DataArray` objects with the `==` operator. The script captures the initial state of the `attrs` dictionary by storing the value of the `units` attribute. It then performs the equality comparison that is suspected to cause the issue. After the comparison, it checks if the `units` attribute has changed. If it has, the script raises an `AssertionError`, indicating the presence of the issue. If no exception is raised and the attributes remain unchanged, it prints a success message and exits with code 0, indicating that the issue has been fixed or is not present.