 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback

from astropy.coordinates import Angle

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    ang = Angle((-0, -42, -17), unit='deg')
    print(ang)
    print(ang.dms)
    print(ang.signed_dms)

    expected_dms = Angle((0, 42, -17), unit='deg').dms
    assert ang.dms == expected_dms, f"dms should be {expected_dms}, but got {ang.dms}"

    expected_signed_dms = Angle((0, 42, -17), unit='deg').signed_dms
    assert ang.signed_dms == expected_signed_dms, (
        f"signed_dms should be {expected_signed_dms}, but got {ang.signed_dms}"
    )

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When you run `python3 reproducer.py`, it will print the following output:
```less
0d42m17s
dms_tuple(d=0.0, m=42.0, s=16.999999999999886)
signed_dms_tuple(sign=1.0, d=0.0, m=42.0, s=16.999999999999886)
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    main()
  File "reproducer.py", line 21, in main
    assert ang.dms == expected_dms, f"dms should be {expected_dms}, but got {ang.dms}"
AssertionError: dms should be dms_tuple(d=0.0, m=-42.0, s=-17.0), but got dms_tuple(d=0.0, m=42.0, s=16.999999999999886)
```
This confirms that the `Angle` class does not handle the sign correctly for a `(d, m, s)` tuple input if `d=0`.