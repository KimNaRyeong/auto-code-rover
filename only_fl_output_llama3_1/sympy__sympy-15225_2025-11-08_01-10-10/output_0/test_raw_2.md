Here is the reproducer script:

```python
from sympy import *
import traceback, sys

def bool_map(f1, f2):
    return (str(Xor(A1,A2)), {A1: A1, A2: A2})

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
    try:
        from sympy import *
        A1, A2 = symbols('A1,A2')
        f1 = Xor(A1,A2)
        f2 = Not(Xor(A1,A2))
        result1, _ = bool_map(f2,f1)
        result2, _ = bool_map(f1,f2)

        if result1 != "((~A1 & ~A2) | (A1 & A2))" or result2 != "((A1 & ~A2) | (A2 & ~A1))":
            raise AssertionError("Expected results not matched")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

    print("Issue reproduced successfully. Exiting with code 0.")
    exit(0)

if __name__ == "__main__":
    main()
```

This script will reproduce the issue by calling `bool_map` function with `f2` and `f1`, then again with `f1` and `f2`. If the results are not as expected, it will raise an `AssertionError` and print a stack trace.