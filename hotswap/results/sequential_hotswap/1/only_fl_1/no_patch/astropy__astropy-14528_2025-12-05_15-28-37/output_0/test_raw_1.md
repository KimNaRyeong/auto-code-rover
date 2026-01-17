 Here is a standalone python file `reproducer.py` to reproduce the issue:
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
    hdu = fits.ImageHDU(name='test', data=np.array(1.0))
    hdu.writeto(filename, overwrite=True)
    with fits.open(filename) as hdul:
        data = hdul[0].data
    assert np.shape(data) == (), "The data should be zero-dimensional."
    assert data == 1.0, "The data should be 1.0."

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line numbers of the statements. The script will also exit with code 1 to indicate that an error occurred.

The issue is present in the line `hdu.writeto(filename, overwrite=True)`, which silently creates a corrupt FITS file when the `data` array is zero-dimensional. The expected behavior is for `io.fits` to raise an error or warning in this situation, rather than silently creating a corrupt file.