 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
import traceback

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

class ZeroMatrix:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols

    def as_explicit(self):
        return [[0]*self.cols for _ in range(self.rows)]

    def __nonzero__(self):
        return False
