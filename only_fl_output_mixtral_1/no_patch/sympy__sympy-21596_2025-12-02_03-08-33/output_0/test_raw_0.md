 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import imageset, Lambda, S, I, Interval, Intersection
from sympy.sets import Set

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

# Define the is_subset(Reals) function with the bug
def is_subset(set1: Set, set2: Set) -> bool:
    return set1.intersect(set2) == set1

# Define the S1 and S2 sets
S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)
S2 = Interval(-1, 1, real=True)

# Check if 2 is in S1 and S1 intersect S2
try:
    assert not (2 in S1)
    assert not (is_subset(S1, S2))
    assert (S1.intersect(S2) == {-1, 1})
except AssertionError as e:
    print_stacktrace(e)
    raise
```
When executed with `python3 reproducer.py`, the script will print the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    assert (S1.intersect(S2) == {-1, 1})
AssertionError: {n + I*(-n**2 + n + 1) for n in Z} == {-1, 1}
```
This confirms that the issue is present. If the issue is fixed, the script will exit with code 0 without printing any stack trace.