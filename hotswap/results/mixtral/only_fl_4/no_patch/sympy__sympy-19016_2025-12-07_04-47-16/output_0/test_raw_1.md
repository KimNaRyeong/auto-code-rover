 Here is a standalone Python file `reproducer.py` to reproduce the first issue:
```python
from sympy import Range

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

try:
    r = Range(5)
    if not r.is_finite_set:
        raise AssertionError("is_finite_set property not implemented for Range")
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` and print a stack trace showing the line number of the statement that caused the issue.

Regarding the second issue, it seems that the `sup` and `inf` methods are not implemented for ranges with symbolic integers. To reproduce this issue, you can use the following `reproducer.py`:
```python
from sympy import Symbol, oo, Range

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

try:
    n = Symbol('n', integer=True)
    s = Range(n, oo, 1)
    sup = s.sup
    inf = s.inf
except Exception as e:
    print_stacktrace(e)
```
When executed with `python3 reproducer.py`, the script will print a stack trace showing the line number of the statement that caused the issue.

To fix the second issue, you can implement the `sup` and `inf` methods for ranges with symbolic integers. One possible implementation is to use the `max` and `min` functions, respectively, to find the maximum and minimum values in the range. Here is an example implementation:
```python
@property
def sup(self):
    if any(not x.is_number for x in self.args):
        raise ValueError("Cannot find supremum of a range with symbolic integers")
    return max(self.args)

@property
def inf(self):
    if any(not x.is_number for x in self.args):
        raise ValueError("Cannot find infimum of a range with symbolic integers")
    return min(self.args)
```
Note that this implementation assumes that the range has a finite number of elements. If the range has an infinite number of elements, then the `sup` and `inf` methods should return `oo` and `-oo`, respectively.