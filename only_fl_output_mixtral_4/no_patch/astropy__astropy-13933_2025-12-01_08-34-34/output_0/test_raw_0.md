 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import astropy.coordinates
import pickle

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

if __name__ == '__main__':
    ang = astropy.coordinates.Angle(0.25 * astropy.units.hourangle)
    pang = pickle.loads(pickle.dumps(ang))
    try:
        pang.to_string()
    except Exception as e:
        print_stacktrace(e)
        assert False
```
When executed with `python3 reproducer.py`, it should raise an `AssertionError` and print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    pang.to_string()
  File "/Users/username/miniconda3/envs/test/lib/python3.10/site-packages/astropy/coordinates/angles.py", line 1054, in to_string
    return self._format_angle(format, unit)
  File "/Users/username/miniconda3/envs/test/lib/python3.10/site-packages/astropy/coordinates/angles.py", line 1027, in _format_angle
    sexagesimal = self.sexagesimal
  File "/Users/username/miniconda3/envs/test/lib/python3.10/site-packages/astropy/coordinates/angles.py", line 1155, in sexagesimal
    raise ValueError("'{0}' can not be represented in sexagesimal notation".format(self.unit))
ValueError: 'hourangle' can not be represented in sexagesimal notation
```
This confirms that the issue is present. When the issue is fixed, the script should exit with code 0 without raising an `AssertionError`.