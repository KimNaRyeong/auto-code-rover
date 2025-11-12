Here is the standalone Python script `reproducer.py` to reproduce the issue:
```python
import io
import numpy as np
from astropy.table import Table, Column

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

try:
    dtype = np.dtype([('z', 'f8'), ('name', 'f8'), ('y', 'i4')])
    t = Table()
    t['c'] = Column([(1, 2, 3), (4, 5, 6)], dtype=dtype)
    out = io.StringIO()
    t.write(out, format='ascii.ecsv')
    print(out.getvalue())
    t2 = Table.read(out.getvalue(), format='ascii.ecsv')
    assert t.equals(t2)  # Check if round-trip is successful
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Structured column serialization round-trip failed")
```
This script reproduces the issue by creating a table with a structured column, serializing it to ECSV, and then reading it back. If the round-trip is successful, it asserts that the original table equals the read-back table. If an exception occurs during this process, it prints the stack trace using the `print_stacktrace` function and raises an `AssertionError`.