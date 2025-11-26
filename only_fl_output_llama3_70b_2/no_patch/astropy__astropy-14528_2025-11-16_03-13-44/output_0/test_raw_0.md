Here is the standalone Python script `reproducer.py` to reproduce the issue:
```
import numpy as np
from astropy.io import fits

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
    filename = 'corrupted.fits'
    hdu = fits.ImageHDU(name='test', data=np.array(1.0))
    hdu.writeto(filename, overwrite=True)

    try:
        with fits.open(filename) as hdul:
            hdul.verify()
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Corrupt FITS file created")

if __name__ == "__main__":
    main()
```
This script creates a zero-dimensional `ImageHDU` and writes it to a file. Then, it tries to open the file using `fits.open` and verify its integrity using `hdul.verify()`. If an exception is raised during verification, it prints the stack trace of the issue and raises an `AssertionError`.