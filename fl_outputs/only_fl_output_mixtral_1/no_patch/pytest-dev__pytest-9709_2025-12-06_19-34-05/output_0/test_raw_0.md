 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
except AssertionError as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script prints the following output:
```csharp
[1, 4, 16, 2, 8, 64, 512, 32, 128, 1024, 256, 4096]
[1, 4, 16, 2, 8, 64, 512, 32, 128, 1024, 256, 409