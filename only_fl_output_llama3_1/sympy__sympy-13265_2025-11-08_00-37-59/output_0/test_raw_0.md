Here is the reproducer script:

```python
import sympy as sp
from sympy import sin, cos, exp, Matrix
from sympy.simplify.fu import fu
from sympy.simplify.sqrtdenest import sqrtdenest
from sympy.simplify.trigsimp import trigsimp

def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def reproduce_issue():
    m = exp(Matrix([[0, -1, 0], [1, 0, 0], [0, 0, 0]]))
    try:
        simplified_m = sp.simplify(m)
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

if __name__ == "__main__":
    reproduce_issue()
```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`. The script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.