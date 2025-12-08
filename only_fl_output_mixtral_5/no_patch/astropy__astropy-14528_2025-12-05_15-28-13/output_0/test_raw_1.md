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

filename = 'corrupted.fits'
hdu = fits.ImageHDU(name='test', data=np.array(1.0))
hdu.writeto(filename, overwrite=True)

try:
    fits.getdata(filename)
except Exception as e:
    print_stacktrace(e)
    assert False, "An exception should have been raised before this point."
```
When executed with `python3 reproducer.py`, the script will print a stack trace and exit with code 1, indicating that the issue is present.

The expected behavior is for `fits.getdata(filename)` to raise an exception before reaching the assertion statement, indicating that the FITS file is corrupt. This would require a fix in the `astropy.io.fits` library to handle the case of zero-dimensional data arrays more gracefully.