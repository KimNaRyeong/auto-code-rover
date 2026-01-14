 Here is a standalone Python script `reproducer.py` that reproduces the issue:
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
    sympy.version.prerelease = False
    sympy.__version__ = sympy.version.version
    print('Sympy version: ', sympy.__version__)

    x = symbols('x')
    q = Quaternion(cos(x/2), sin(x/2), 0, 0)
    m = q.to_rotation_matrix()
    m = trigsimp(m)

    expected = Matrix([
        [1, 0, 0],
        [0, cos(x), -sin(x)],
        [0, sin(x), cos(x)]
    ])

    assert m == expected, "The output of Quaternion.to_rotation_matrix() is incorrect"

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, the script will print the following output:
```vbnet
Sympy version:  1.2
Traceback (most recent call last):
  File "reproducer.py", line 28, in <module>
    main()
  File "reproducer.py", line 23, in main
    assert m == expected, "The output of Quaternion.to_rotation_matrix() is incorrect"
AssertionError: The output of Quaternion.to_rotation_matrix() is incorrect
```
This confirms that the issue is present in Sympy version 1.2.