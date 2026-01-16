```python
# reproducer.py
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

def test_wcslint_issue_1():
    from astropy.io import fits
    from astropy.wcs import WCS

    try:
        # Modify the following path to point to the actual FITS file downloaded from the example URI
        fits_path = 'path_to_your_fits_file/jbqf03gjq_flc.fits'
        hdu_list = fits.open(fits_path)
        header = hdu_list[1].header  # Assuming the issue occurs with the first HDU after the PRIMARY
        wcs_obj = WCS(header)
        print("First test passed: WCS object was created successfully.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("First test failed: Exception occurred while creating WCS object.") from e

def test_wcslint_issue_2():
    from astropy.io import fits
    from astropy.wcs import WCS

    try:
        # Modify the following path to point to the actual FITS file downloaded from the example URI
        fits_path = 'path_to_your_fits_file/tab-time-last-axis.fits'
        hdu_list = fits.open(fits_path, memmap=False)  # Ensure memmap is False to prevent lazy loading issues
        wcs_obj = WCS(hdu_list[1].header, hdu_list=hdu_list)
        print("Second test passed: WCS object with HDUList was created successfully.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Second test failed: Exception occurred with -TAB coordinates or indices.") from e

def test_wcslint_issue_3():
    from astropy.io import fits
    from astropy.wcs import WCS

    try:
        # Modify the following path to point to the actual FITS file downloaded from the example URI
        fits_path = 'path_to_your_fits_file/iabj01a2q_flc.fits'
        hdu_list = fits.open(fits_path)
        wcs_obj = WCS(hdu_list[1].header)
        print("Third test passed: WCS object was created successfully with SIP distortion.")
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Third test failed: Exception occurred with SIP distortion coefficients.") from e

if __name__ == "__main__":
    test_functions = [test_wcslint_issue_1, test_wcslint_issue_2, test_wcslint_issue_3]
    for test_func in test_functions:
        try:
            test_func()
        except AssertionError as e:
            print(f"AssertionError in {test_func.__name__}: {str(e)}")
            sys.exit(1)  # Exit with error if any test fails
    sys.exit(0)  # Exit cleanly if all tests pass
```

Before running `reproducer.py`, make sure to download the FITS files mentioned in the issue and adjust the `fits_path` in each test function to point to the correct file locations on your system. This script attempts to reproduce the outlined issues by creating WCS objects with the headers from the specified FITS files and validates the behavior based on the descriptions provided.