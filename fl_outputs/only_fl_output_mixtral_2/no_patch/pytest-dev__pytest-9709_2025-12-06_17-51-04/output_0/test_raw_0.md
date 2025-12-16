 Here is a standalone Python file `reproducer.py` to reproduce the issue:
```python
import numpy as np
import pytest

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

a = 2**np.arange(12)
b = 2**np.arange(12)
np.random.shuffle(a)

print(a)
print(b)

print(*set(a))
print(*set(b))

try:
    print(set(a) == pytest.approx(set(b)))
except AssertionError:
    print_stacktrace(e=pytest.UsageError(message="Sets cannot be compared using pytest.approx()."))
except Exception as e:
    print_stacktrace(e=e)
else:
    print("The issue is not reproduced.")
```
When executed with `python3 reproducer.py`, the script will print a stack trace with the line numbers of the statements:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 23
    print(set(a) == pytest.approx(set(b)))
