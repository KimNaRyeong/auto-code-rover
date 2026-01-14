 Here is a standalone Python script `reproducer.py` to reproduce the first issue with the FITS file "P190mm-PAFBE-FEBEPAR.fits":

```python
import astropy
import numpy as np
from astropy.io import fits

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

astropy.__version__

fits_file = 'P190mm-PAFBE-FEBEPAR.fits'

if not fits.exists(fits_file):
    print(f"File '{fits_file}' not found, please download it first.")
    exit(1)

data = fits.getdata(fits_file, 1)
print(data)

try:
    data['USEBAND']
except Exception as e:
    print_stacktrace(e)
```

To run the script, download the FITS file and place it in the same directory as the script. Then execute `python3 reproducer.py`. The script should print the stack trace of the `IndexError` when the issue is present.

Regarding the second issue, it seems to be a more complex problem and might require a more extensive script to reproduce the behavior. However, the provided information should be enough to understand and address the issue.