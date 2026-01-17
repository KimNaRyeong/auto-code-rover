```python
import numpy as np
from astropy.io import fits
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
    filename = 'corrupted.fits'
    try:
        # Create a FITS file with an ImageHDU containing zero-dimensional data
        hdu = fits.ImageHDU(name='test', data=np.array(1.0))
        hdu.writeto(filename, overwrite=True)
        
        # Attempt to read the data back
        data = fits.getdata(filename)
        
        # Check if the data read back matches the data written
        assert np.array_equal(data, np.array(1.0)), "Data mismatch!" 
    except AssertionError as e:
        print("Issue detected: Data read from FITS file does not match data written.")
        print_stacktrace(e)
        sys.exit(1)
    except Exception as e:
        print("Unexpected error occurred.")
        print_stacktrace(e)
        sys.exit(1)
    else:
        print("No issue detected. The FITS file is valid.")
        sys.exit(0)

if __name__ == "__main__":
    main()
```