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
    from astropy.io import fits

    # Issue 1: Reading FITS with variable length columns
    def read_issue():
        data = fits.getdata('P190mm-PAFBE-FEBEPAR.fits', 1)
        # Access to trigger potential IndexError
        _ = data['USEFEED']

    # Issue 2: Writing and Reading Multi-dimensional VLA
    def write_read_issue():
        array = np.array([np.ones((8, 50))], dtype=object)
        col = fits.Column(name='test', format='PD()', array=array)
        fits.BinTableHDU.from_columns([col]).writeto('bug.fits', overwrite=True)

        with fits.open('bug.fits') as hdus:
            data_read = hdus[1].data['test']
            # Access to data to trigger potential error
            _ = data_read[0]

    try:
        read_issue()
    except Exception as e:
        print("Read Issue Encountered:")
        print_stacktrace(e)
    
    try:
        write_read_issue()
    except Exception as e:
        print("Write/Read Issue Encountered:")
        print_stacktrace(e)

except ImportError as e:
    print_stacktrace(e)
    raise AssertionError("Necessary module not found. Please ensure numpy and astropy are installed.") from None
