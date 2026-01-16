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
    try:
        from astropy.wcs import WCS
        
        wcs = WCS(naxis=1)
        
        # This line should raise the IndexError if the bug is present
        result = wcs.all_pix2world(29, 0)
        
        # If the IndexError was not raised, implying the function executed without error
        print("Issue appears to be fixed.")
        exit(0)
    
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("The issue is still present.") from e

if __name__ == "__main__":
    main()
