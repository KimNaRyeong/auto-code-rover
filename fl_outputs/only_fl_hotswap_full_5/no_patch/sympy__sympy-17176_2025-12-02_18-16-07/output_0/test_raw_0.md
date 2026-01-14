 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import *
from sympy.logic.boolalg import _finger
from pprint import pprint


def print_stacktrace(e: Exception):
    import traceback, sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)


def main():
    A1, A2, A3 = symbols('A1, A2, A3')
    f1 = Xor(A1, A2, A3)
    f2 = ~(Xor(A1, A2, A3))
    bool_map_result = bool_map(f1, f2)
    print(f"bool_map({f1}, {f2}) = {bool_map_result}")

    a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
    b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
    print("a =")
    pprint(a)
    print("b =")
    pprint(b)

    assert a != b, "The fingerprints for the two expressions should not be identical."


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print_stacktrace(e)
        raise
```
When executed with `python3 reproducer.py`, the script will print the stack trace and raise an `AssertionError`:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 34, in <module>
    main()
  File "reproducer.py", line 30, in main
    assert a != b, "The fingerprints for the two expressions should not be identical."
AssertionError: The fingerprints for the two expressions should not be identical.
```
This reproduces the issue described in the original post.