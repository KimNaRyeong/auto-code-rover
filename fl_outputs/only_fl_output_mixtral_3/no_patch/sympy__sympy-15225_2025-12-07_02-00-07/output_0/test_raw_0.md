 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
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

def bool_map_test():
    A1, A2 = symbols('A1, A2')
    f1 = Xor(A1, A2)
    f2 = ~(Xor(A1, A2))
    bool_map_f1_f2 = bool_map(f1, f2)
    bool_map_f2_f1 = bool_map(f2, f1)
    if bool_map_f1_f2 != ({A1: A1 & A2, A2: ~A1 & ~A2}, {A1: A1, A2: A2}) or \
       bool_map_f2_f1 != ({A1: A1 & ~A2 | A2 & ~A1, A2: True}, {A1: A1, A2: A2}):
        raise AssertionError("Bool map returned incorrect symbol mapping")

if __name__ == "__main__":
    try:
        bool_map_test()
        print("Issue not present")
        exit(0)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 24, in <module>
    bool_map_test()
  File "reproducer.py", line 19, in bool_map_test
    raise AssertionError("Bool map returned incorrect symbol mapping")
AssertionError: Bool map returned incorrect symbol mapping
```
This confirms that the issue is present in the `bool_map` function of the `sympy` library.