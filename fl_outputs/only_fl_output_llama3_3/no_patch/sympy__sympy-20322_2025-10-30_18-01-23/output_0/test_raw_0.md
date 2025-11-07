Here is the reproducer script:

```python
import sympy
from unittest import TestCase

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

class Reproducer(TestCase):
    def test_ceiling_issue(self):
        sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
        sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=True).simplify()

if __name__ == "__main__":
    try:
        Reproducer().test_ceiling_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

```

To run the script, save it to a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.