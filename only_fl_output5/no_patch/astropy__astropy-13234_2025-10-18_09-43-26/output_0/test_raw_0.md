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

def main():
    import io
    import numpy as np
    from astropy.table import Table, Column

    dtype = np.dtype([('z', 'f8'), ('name', 'f8'), ('y', 'i4')])
    t = Table()
    t['c'] = Column([(1, 2, 3), (4, 5, 6)], dtype=dtype)

    out = io.StringIO()
    t.write(out, format='ascii.ecsv')

    out.seek(0)  # Reset StringIO's internal pointer to the beginning

    try:
        t2 = Table.read(out.getvalue(), format='ascii.ecsv')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue with structured column serialization round-trip with field name 'name'") from e

if __name__ == "__main__":
    main()
```

This script is designed to reproduce the issue described. It attempts to round-trip a table with a structured column through the ECSV format. If the issue exists (identified by failing to correctly deserialize the column with the field name 'name'), it will print the stack trace of the error encountered and raise an `AssertionError`. The script is intended to exit with code 0 (success) when the problem is fixed, meaning no error should be raised in that scenario.