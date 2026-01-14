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
    sympy.version.prerelease = False  # ensure stable version
    print('Sympy version: ', sympy.__version__)

    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    expected_matrix = Matrix([
        [1, 0, 0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])

    try:
        actual_matrix = trigsimp(q.to_rotation_matrix())
        if actual_matrix != expected_matrix:
            raise AssertionError(f"Expected {expected_matrix}, but got {actual_matrix}")
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    main()
```
This script sets the Sympy version to a stable release, defines the expected rotation matrix, and compares it to the actual matrix obtained from the `Quaternion.to_rotation_matrix()` method. If the matrices are not equal, an `AssertionError` is raised, and the `print_stacktrace` function prints the stack trace.

To run the script, execute `python3 reproducer.py`. If the issue is present, the script will print the stack trace and exit with code 1. If the issue is fixed, the script will exit with code 0.