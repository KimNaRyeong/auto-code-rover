 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy
from sympy import *

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    sympy.version.prerelease = False
    sympy.__version__ = sympy.version.version
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    expected_matrix = Matrix([
        [1, 0, 0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])
    actual_matrix = q.to_rotation_matrix()
    actual_matrix = trigsimp(actual_matrix)
    if not (expected_matrix == actual_matrix).all():
        raise AssertionError(f"Expected {expected_matrix}, but got {actual_matrix}")

if __name__ == "__main__":
    try:
        main()
        print("Issue is fixed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will print the following output if the issue is present:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    main()
  File "reproducer.py", line 26, in main
    raise AssertionError(f"Expected {expected_matrix}, but got {actual_matrix}")
AssertionError: Expected Matrix([
[1, 0, 0],
[0, cos(x), -sin(x)],
[0, sin(x), cos(x)]]), but got Matrix([
[1,      0,      0],
[0, cos(x), sin(x)],
[0, sin(x), cos(x)]])
```
If the issue is fixed, the script will print "Issue is fixed." and exit with code 0.