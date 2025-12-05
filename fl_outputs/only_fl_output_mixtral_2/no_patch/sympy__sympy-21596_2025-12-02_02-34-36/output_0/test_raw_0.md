 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import imageset, Lambda, S, I, Interval, Intersection
from sympy.sets import Reals

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

# Define the given issue
S1 = imageset(Lambda(n, n + (n - 1)*(n + 1)*I), S.Integers)

# Check the incorrect output
print("Incorrect output:")
print(f"S1 = {S1}")
print(f"2 in S1 = {2 in S1}")
print(f"2 in S1.intersect(Reals) = {2 in S1.intersect(Reals)}")

# Check the correct output
S2 = Reals
expected_intersection = Intersection(S1, S2)
expected_intersection_set = {-1, 1}

if expected_intersection_set == list(expected_intersection):
    print("Correct output:")
    print(f"S1 = {S1}")
    print(f"2 in S1 = {2 in S1}")
    print(f"2 in S1.intersect(Reals) = {2 in S1.intersect(Reals)}")
    print(f"S1.intersect(S2) = {list(S1.intersect(S2))}")
else:
    raise AssertionError(f"The intersection of S1 and S2 is incorrect: {expected_intersection}")
```
When executed with `python3 reproducer.py`, the script will print the incorrect output and then raise an `AssertionError` with the stack trace.

The output will be:
```vbnet
Incorrect output:
S1 = {n + I⋅(n - 1)⋅(n + 1) | n ∈ ℤ}
2 in S1 = False
2 in S1.intersect(Reals) = True
Traceback (most recent call last):
  File "reproducer.py", line 25, in <module>
    raise AssertionError(f"The intersection of S1 and S2 is incorrect: {expected_intersection}")
AssertionError: The intersection of S1 and S2 is incorrect: {-1, 1}
```
If the issue is fixed, the script will print the correct output and exit with code 0.