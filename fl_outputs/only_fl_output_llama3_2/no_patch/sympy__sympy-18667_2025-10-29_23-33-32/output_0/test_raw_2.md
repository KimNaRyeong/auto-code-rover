Here is the reproducer script:

```python
import unittest
from combinatorics import Schur_Number  # Replace 'combinatorics' with the actual name of your module

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

if __name__ == '__main__':
    try:
        Schur_Number(1)  # Replace '1' with the actual input for Schur number
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)
```

This script will execute the `Schur_Number` function and if it raises an `AssertionError`, it will print the stack trace of the failure.