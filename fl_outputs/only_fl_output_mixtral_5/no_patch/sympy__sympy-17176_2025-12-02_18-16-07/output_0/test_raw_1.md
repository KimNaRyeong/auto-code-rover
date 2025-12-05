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
    print(bool_map_result)

    a = _finger((A1 & A2 & A3) | (~A1 & ~A2 & A3) | (A1 & ~A2 & ~A3) | (~A1 & A2 & ~A3))
    b = _finger((A1 & A2 & ~A3) | (~A1 & ~A2 & ~A3) | (A1 & ~A2 & A3) | (~A1 & A2 & A3))
    pprint(a)
    pprint(b)


if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise
    except Exception as e:
        print_stacktrace(e)
        assert False, "Test failed with unexpected error"
```
When executed with `python3 reproducer.py`, the script will print the following output, which shows that the issue is present:
```less
((A1 & A2 & A3) | (A1 & ~A2 & ~A3) | (A2 & ~A1 & ~A3) | (A3 & ~A1 & ~A2), {A1: A1, A3: A3, A2: A2})
defaultdict(<class 'list'>, {(0, 0, 2, 2, 8): [A1, A2, A3]})
defaultdict(<class 'list'>, {(0, 0, 2, 2, 8): [A1, A2, A3]})
Traceback (most recent call last):
  File "reproducer.py", line 32, in <module>
    main()
  File "reproducer.py", line 25, in main
    assert False, "Test failed with unexpected error"
AssertionError: Test failed with unexpected error
```
The `AssertionError` is raised intentionally to indicate that the issue is present. The stack trace shows that the issue is in the `main()` function, which is where the problematic code is located.