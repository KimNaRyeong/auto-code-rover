Here is the reproducer script:

```python
import numpy as np
import astropy.wcs
from astropy.coordinates import SkyCoord
import astropy.units as u

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

try:
    import numpy as np
    from astropy.wcs import WCS

    nx = 100
    ny = 25
    nz = 2
    wcs_header = {
        'WCSAXES': 3,
        'CRPIX1': (nx + 1)/2,
        'CRPIX2': (ny + 1)/2,
        'CRPIX3': 1.0,
        'PC1_1': 0.0,
        'PC1_2': -1.0,
        'PC1_3': 0.0,
        'PC2_1': 1.0,
        'PC2_2': 0.0,
        'PC2_3': -1.0,
        'CDELT1': 5,
        'CDELT2': 5,
        'CDELT3': 0.055,
        'CUNIT1': 'arcsec',
        'CUNIT2': 'arcsec',
        'CUNIT3': 'Angstrom',
        'CTYPE1': 'HPLN-TAN',
        'CTYPE2': 'HPLT-TAN',
        'CTYPE3': 'WAVE',
        'CRVAL1': 0.0,
        'CRVAL2': 0.0,
        'CRVAL3': 1.05,
    }
    fits_wcs = WCS(header=wcs_header)

    pt = SkyCoord(Tx=0*u.arcsec, Ty=0*u.arcsec, frame=astropy.wcs.utils.wcs_to_celestial_frame(fits_wcs))
    ll_sliced_wcs = astropy.wcs.wcsapi.SlicedLowLevelWCS(fits_wcs, 0)
    hl_sliced_wcs = astropy.wcs.wcsapi.HighLevelWCSWrapper(ll_sliced_wcs)

    assert hl_sliced_wcs.world_to_pixel(pt) == (array(49.5), array(12.), array(2.44249065e-15))

except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script should reproduce the issue and raise an `AssertionError` when the issue is present, and it will print a stack trace of the issue.