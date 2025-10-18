```python
# reproducer.py

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

def reproduce_issue():
    import io
    import numpy as np
    from astropy.table import Table, Column
    
    dtype = np.dtype([('z', 'f8'), ('name', 'f8'), ('y', 'i4')])
    t = Table()
    t['c'] = Column([(1, 2, 3), (4, 5, 6)], dtype=dtype)
    out = io.StringIO()
    t.write(out, format='ascii.ecsv')
    out.seek(0)  # Reset StringIO object to start
    try:
        t2 = Table.read(out.getvalue(), format='ascii.ecsv')
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Failed to round-trip a structured column with field name of 'name' through ECSV.")

if __name__ == "__main__":
    reproduce_issue()
```

This script, `reproducer.py`, is designed to test the specific issue of round-tripping a structured column with a field name of 'name' through the ECSV format using Astropy's Table class. It will raise an `AssertionError` and print a detailed stack trace if the problem is encountered, indicating the issue is present. If the issue has been resolved and the script does not raise an exception, it means the bug has been fixed and the script will exit with code 0, confirming the successful resolution.