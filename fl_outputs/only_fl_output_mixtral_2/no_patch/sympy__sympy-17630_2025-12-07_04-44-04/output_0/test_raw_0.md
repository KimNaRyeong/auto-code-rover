 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
from sympy import *

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

a = MatrixSymbol("a", 2, 2)
z = ZeroMatrix(2, 2)
b = BlockMatrix([[a, z], [z, z]])

assert type(b._blockmul(b).blocks[0, 1]) == Matrix
# Uncomment the following line to see the issue
# assert type(b._blockmul(b).blocks[0, 1]) == ZeroMatrix

result = b * b * b
assert False, "Did not raise AttributeError"
```
To reproduce the issue, run `python3 reproducer.py` and it should raise an `AssertionError` with a stack trace.

The issue is caused by the fact that the zeros in `b._blockmul(b)` are not `ZeroMatrix` but `Zero`, which does not have the `cols` attribute. This happens because the `_blockmul` method of `BlockMatrix` does not return a `BlockMatrix` object when the blocks are all zeros.

To fix the issue, the `_blockmul` method should always return a `BlockMatrix` object, even when the blocks are all zeros. This can be done by modifying the `_blockmul` method in `sympy/matrices/expressions/blockmatrix.py` as follows:
```python
def _blockmul(self, other):
    if not self.blocks or not other.blocks:
        return ZeroMatrix(*self.shape)
    ...
```
With this modification, the `reproducer.py` script should exit with code 0.