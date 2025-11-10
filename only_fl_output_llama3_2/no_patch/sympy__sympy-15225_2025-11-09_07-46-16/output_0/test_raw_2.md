Here is the reproducer script:

```python
from sympy import *

def main():
    A1, A2 = symbols('A1,A2')
    f1 = Xor(A1, A2)
    f2 = Not(Xor(A1, A2))
    
    try:
        print(bool_map(f2, f1))
        print(bool_map(f1, f2))
    except Exception as e:
        print_stacktrace(e)
        raise AssertionError("Issue not fixed")

def bool_map(f1, f2):
    from sympy import Not
    return (f"({') | ('.join(map(str, [Not(x) if x else x for x in reduce(or_, map(lambda x: x if isinstance(x, Symbol) else Xor(*x.args), f1.args)])))))", {str(k): str(v) for k, v in zip(f1.free_symbols, f2.free_symbols)}

def print_stacktrace(e):
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

if __name__ == "__main__":
    main()
```

This script will run the given code and check if it raises an exception. If it does, it will print a stack trace and then raise an `AssertionError`.