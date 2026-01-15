```python
import sys

def print_stacktrace(e: Exception):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    try:
        from astropy.io import fits
        from astropy.wcs import WCS
        import os

        # Example fits file URLs (assuming already downloaded for the sake of demonstration).
        # Replace the paths with the actual location of the FITS files on your system.
        fits_files = ['jbqf03gjq_flc.fits', 'tab-time-last-axis.fits', 'iabj01a2q_flc.fits']
        
        for fits_file in fits_files:
            with fits.open(fits_file) as hdul:
                header = hdul[1].header  # Assuming the primary target is in the first extension.
                try:
                    wcs = WCS(header)
                    assert False, "Expected to encounter an error before this assertion."
                except AssertionError as ae:
                    raise ae  # This is the AssertionError for the issue presence check.
                except Exception as e:
                    # If an exception occurs, it indicates the issue is present.
                    print(f"Error encountered with: {fits_file}")
                    print_stacktrace(e)
    except Exception as e:
        print("An unexpected error occurred:", e)
        sys.exit(1)

if __name__ == "__main__":
    main()
```

This script attempts to reproduce the issue by loading the WCS information from FITS files you've described as problematic. You need to download those files and update the `fits_files` list with the correct path to these files on your system. When the issue exists in the WCS or its usage, as detailed in your problem statement, the intended errors will be caught and displayed using the provided `print_stacktrace` function.

Please note the `AssertionError` with a message "Expected to encounter an error before this assertion." is a placeholder, assuming that reaching it means the specific issue was supposed to happen before and thus signaling an unexpected condition (e.g., if some updates or fixes cause the script not to fail as before). Remember, real debugging involves more nuances and may require additional information or steps depending on the context of the error.