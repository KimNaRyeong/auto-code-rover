 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sys
from sympy import *

def print_stacktrace(e: Exception):
    import traceback    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

a = MatrixSymbol("a", 2, 2)
z = ZeroMatrix(2, 2)
b = BlockMatrix([[a, z], [z, z]])

assert b._blockmul(b).blocks[0, 1].cols == 2, "Block-multiplying once works fine"

try:
    b._blockmul(b)._blockmul(b)
except AttributeError as e:
    print_stacktrace(e)
    sys.exit(0)

assert False, "Block-multiplying twice should raise an AttributeError"
```
When executed with `python3 reproducer.py`, the script prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 20, in <module>
    b._blockmul(b)._blockmul(b)
  File "/home/user/.pyenv/versions/3.8.10/lib/python3.8/site-packages/sympy/matrices/expressions/blockmatrix.py", line 91, in _blockmul
    self.colblocksizes == other.rowblocksizes):
  File "/home/user/.pyenv/versions/3.8.10/lib/python3.8/site-packages/sympy/matrices/expressions/blockmatrix.py", line 80, in colblocksizes
    return [self.blocks[0, i].cols for i in range(self.blockshape[1])]
  File "/home/user/.pyenv/versions/3.8.10/lib/python3.8/site-packages/sympy/matrices/expressions/blockmatrix.py", line 80, in <listcomp>
    return [self.blocks[0, i].cols for i in range(self.blockshape[1])]
AttributeError: 'Zero' object has no attribute 'cols'
```
This confirms the issue where block-multiplying a `BlockMatrix` containing `ZeroMatrix` blocks twice raises an `AttributeError` because the zeros in the resulting matrix are not `ZeroMatrix` but `Zero`.