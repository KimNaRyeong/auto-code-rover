```python
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

def test_structured_column_serialization_roundtrip():
    import io
    import numpy as np
    from astropy.table import Table, Column

    dtype = np.dtype([('z', 'f8'), ('name', 'f8'), ('y', 'i4')])
    t = Table()
    t['c'] = Column([(1, 2, 3), (4, 5, 6)], dtype=dtype)

    out = io.StringIO()
    
    try:
        t.write(out, format='ascii.ecsv')
        t2 = Table.read(out.getvalue(), format='ascii.ecsv')

        # Assertion to check if round-trip maintains data integrity
        assert np.all(t['c'] == t2['c']), "Round-trip serialization failed"
        print("Round-trip serialization succeeded")
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    try:
        test_structured_column_serialization_roundtrip()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception:
        exit(1)
    else:
        exit(0)
```