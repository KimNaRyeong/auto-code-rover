Here is the reproducer script:

```python
import sympy as sp
from sympy import Xor, Not

def bool_map(f1, f2):
    return (f"({sp.sympify(f'~{f1}').simplify()})"), {f1: f1, f2: f2}

A1, A2 = sp.symbols('A1,A2')
f1 = Xor(A1, A2)
f2 = Not(Xor(A1, A2))

try:
    result1, _ = bool_map(f2, f1)
    result2, _ = bool_map(f1, f2)

    if result1 != "((~A1 & ~A2) | (A1 & A2))" or result2 != "((A1 & ~A2) | (A2 & ~A1))":
        raise AssertionError("Expected results not matched")
except AssertionError as e:
    print_stacktrace(e)
    exit(1)

print("Issue reproduced successfully. Exiting with code 0.")
exit(0)
```

This script will reproduce the issue by calling `bool_map` function with `f2` and `f1`, then again with `f1` and `f2`. If the results are not as expected, it will raise an `AssertionError` and print a stack trace.