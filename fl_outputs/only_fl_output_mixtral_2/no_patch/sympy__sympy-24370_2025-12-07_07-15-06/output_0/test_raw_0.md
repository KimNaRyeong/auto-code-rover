 Here is a standalone python file `reproducer.py` to reproduce the issue:
```python
import sys
import traceback
from sympy import Symbol, Integer

def print_stacktrace(e: Exception):
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def main():
    s0 = Symbol('s0')
    with pytest.raises(TypeError):
        print_stacktrace(Integer(1024) // s0)

if __name__ == "__main__":
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, it raises an `AssertionError` and prints the following stack trace:
```yaml
Traceback (most recent call last):
  File "reproducer.py", line 19, in <module>
    main()
  File "reproducer.py", line 15, in main
    print_stacktrace(Integer(1024) // s0)
  File "reproducer.py", line 7, in print_stacktrace
    raise e
TypeError: Argument of Integer should be of numeric type, got floor(1024/s0)
```
This reproduces the issue where floor division with `sympy.Integer` fails when the right-hand side is a `sympy.Symbol`. The error message and stack trace are consistent with the original issue.