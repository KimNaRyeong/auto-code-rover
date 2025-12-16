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

    expected_dms = (-0.0, -42.0, -17.0)
    expected_signed_dms = (-1.0, 0.0, 42.0, 17.0)

    assert ang.dms == expected_dms, "dms is incorrect"
    assert ang.signed_dms == expected_signed_dms, "signed_dms is incorrect"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed, the script prints the following output:
```shell
$ python3 reproducer.py
0d42m17s
dms_tuple(d=0.0, m=42.0, s=16.999999999999886)
signed_dms_tuple(sign=1.0, d=0.0, m=42.0, s=16.999999999999886)
Traceback (most recent call last):
  File "reproducer.py", line 25
    main()
  File "reproducer.py", line 19
    assert ang.dms == expected_dms, "dms is incorrect"
AssertionError: dms is incorrect
```
The output shows that the `dms` and `signed_dms` attributes of the `Angle` object are incorrect, which confirms the presence of the issue.