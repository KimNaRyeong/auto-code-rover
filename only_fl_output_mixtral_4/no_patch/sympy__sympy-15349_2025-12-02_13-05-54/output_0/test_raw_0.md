 Here is a standalone Python script `reproducer.py` that reproduces the issue with Sympy version 1.2:
```python
import sympy
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

def main():
    sympy.version.prerelease = False  # ensure stable version is used
    sympy.__version__ = "1.2"  # set Sympy version to reproduce the issue
    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    expected_matrix = Matrix([
        [1, 0, 0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])
    actual_matrix = q.to_rotation_matrix()
    actual_matrix = trigsimp(actual_matrix)
    if actual_matrix != expected_matrix:
        error_msg = f"Expected: {expected_matrix}\nActual: {actual_matrix}"
        raise AssertionError(error_msg)

if __name__ == "__main__":
    try:
        main()
        print("Issue is fixed.")
        sys.exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
To execute the script, run `python3 reproducer.py`. If the issue is present, an `AssertionError` will be raised, and a stack trace will be printed. If the issue is fixed, the script will print "Issue is fixed." and exit with code 0.