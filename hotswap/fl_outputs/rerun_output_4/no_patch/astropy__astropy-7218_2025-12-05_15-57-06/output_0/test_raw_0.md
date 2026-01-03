 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from astropy.io.fits import HDUList

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

def main():
    hdulist = HDUList()
    hdulist_copy = hdulist.copy()
    assert type(hdulist_copy) is HDUList, "HDUList.copy() should return an HDUList instance, but got a list instead."

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with Python 3.6, this script should raise an `AssertionError` and print a stack trace of the issue:
```sh
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 15
    main()
  File "reproducer.py", line 11
    hdulist_copy = hdulist.copy()
  File "reproducer.py", line 8
    assert type(hdulist_copy) is HDUList, "HDUList.copy() should return an HDUList instance, but got a list instead."
AssertionError: HDUList.copy() should return an HDUList instance, but got a list instead.
```
When the issue is fixed, this script should exit with code 0 without printing any stack trace.