```python
# reproducer.py
import xarray as xr


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


def test_decode_with_scale_factor_as_list():
    try:
        ds = xr.DataArray([0, 1, 2], name='foo',
                          attrs={'scale_factor': [0.01],
                                 'add_offset': [1.0]}).to_dataset()
        xr.decode_cf(ds)
    except AttributeError as e:
        print_stacktrace(e)
        raise AssertionError("decode_cf fails when scale_factor is a length-1 list") from e
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("An unexpected error occurred") from e


if __name__ == "__main__":
    test_decode_with_scale_factor_as_list()
```