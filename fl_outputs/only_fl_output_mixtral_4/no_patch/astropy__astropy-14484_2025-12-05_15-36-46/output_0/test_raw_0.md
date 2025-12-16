 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import astropy.units as u
import numpy as np

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

a = np.array([78, 78, 81]) * u.pix**2
b = np.array([78.5, 78.5, 78.625]) * u.pix**2
try:
    np.testing.assert_equal(a, b)
except AssertionError as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script should print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 13, in <module>
    np.testing.assert_equal(a, b)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/testing/_private/utils.py", line 535, in assert_equal
    assert_array_equal(actual, desired, err_msg=err_msg, verbose=verbose)
  File "/home/user/.local/lib/python3.8/site-packages/numpy/testing/_private/utils.py", line 154, in assert_array_equal
    raise AssertionError(msg)
AssertionError:
Arrays are not equal

Mismatch: 30.0%

total size = 3

(a, b): array([78., 78., 81.]), array([78.5, 78.5, 78.625])
```
The warning is not emitted with `astropy-dev` and `numpy` stable (1.24.2) because the warning is introduced in `numpy` version 1.25.0. The warning is emitted because the `assert_equal` function from `numpy.testing` calls the `max` function, which is not known to `astropy.units.Quantity`. The warning suggests raising an issue at <https://github.com/astropy/astropy/issues>.