Here is the reproducer script:

```python
import xarray as xr
import numpy as np

def print_stacktrace(e):
    import traceback
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_decode_cf_fails_with_length_1_list():
    ds = xr.DataArray([0, 1, 2], name='foo',
                      attrs={'scale_factor': [0.01],
                             'add_offset': [1.0]}).to_dataset()
    try:
        xr.decode_cf(ds)
    except Exception as e:
        print_stacktrace(e)
        assert False, "Expected decode_cf to fail"

if __name__ == '__main__':
    test_decode_cf_fails_with_length_1_list()
```

This script defines a function `test_decode_cf_fails_with_length_1_list` that creates a dataset with a length-1 list for `scale_factor`, then tries to decode it using `xr.decode_cf`. If an exception is raised, the script prints the stack trace and fails the test.