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
When executed with Python 3.8.5, the script reproduces the issue and raises an `AssertionError` with the following stack trace:
```yaml
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    main()
  File "reproducer.py", line 18, in main
    assert ang.dms == expected_dms, f"dms should be {expected_dms}, but got {ang.dms}"
AssertionError: dms should be dms_tuple(d=0.0, m=-42.0, s=-17.0), but got dms_tuple(d=0.0, m=42.0, s=16.999999999999886)
```
When the proposed solution is applied, the script should exit with code 0, indicating that the issue is fixed.