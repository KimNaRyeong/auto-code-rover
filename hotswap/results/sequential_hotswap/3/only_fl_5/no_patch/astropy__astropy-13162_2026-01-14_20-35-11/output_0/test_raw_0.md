```python
# reproducer.py

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
        from astropy.coordinates import Angle
        ang = Angle((-0, -42, -17), unit='deg')

        # Check if the sign is handled correctly
        assert str(ang) == "-0d42m17s", f"Unexpected angle representation: {ang}"
        dms = ang.dms
        assert dms.d == -0.0 and dms.m == -42.0 and dms.s == -16.999999999999886, "Incorrect DMS representation"
        
        signed_dms = ang.signed_dms
        assert signed_dms.sign == -1.0 and signed_dms.d == 0.0 and \
               signed_dms.m == 42.0 and signed_dms.s == 16.999999999999886, "Incorrect signed DMS representation"

    except AssertionError as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    main()
```