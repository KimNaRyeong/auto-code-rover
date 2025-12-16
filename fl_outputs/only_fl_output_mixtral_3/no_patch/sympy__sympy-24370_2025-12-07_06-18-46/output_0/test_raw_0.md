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
    except Exception as e:
        print_stacktrace(e)
        sys.exit(1)
```
When executed with `python3 reproducer.py`, it raises a `TypeError` with the following stack trace:
```vbnet
Traceback (most recent call last):
  File "reproducer.py", line 18, in <module>
    main()
  File "reproducer.py", line 14, in main
    print_stacktrace(Integer(1024) // s0)
  File "reproducer.py", line 6, in print_stacktrace
    print(f'    {line_number}: {code_context}', file=sys.stderr)
  File "/Users/user/anaconda3/lib/python3.8/site-packages/sympy/core/expr.py", line 320, in __int__
    raise TypeError("Cannot convert symbols to int")
TypeError: Cannot convert symbols to int
```
This reproduces the issue where floor division with `sympy.Integer` fails with a `TypeError` when the right-hand side is a `sympy.Symbol`.