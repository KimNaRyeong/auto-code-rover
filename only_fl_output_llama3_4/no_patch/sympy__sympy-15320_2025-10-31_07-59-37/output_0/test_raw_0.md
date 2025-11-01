Here is the reproducer script in a code block:

```python
import sympy as sp
from reproducer import print_stacktrace

def reproduce_issue():
    x = sp.symbols('x')
    t = sp.symbols('t')

    # Case 1: Same form, different generator
    try:
        root1 = sp.RootOf(x**3 + x - 1, 0)
        root2 = sp.RootOf((x**3 + x - 1).subs(x, t), 0)
        assert root1.poly.gen == x
        print_stacktrace(AssertionError("RootOf might ignore generator"))
    except Exception as e:
        print_stacktrace(e)

    # Case 2: Different form, same generator
    try:
        root3 = sp.RootOf(t**3 + 2*t - 1, 0)
        root4 = sp.RootOf((x**3 + 2*x - 1), 0)
        assert root4.poly.gen == t
        print_stacktrace(AssertionError("RootOf might ignore generator"))
    except Exception as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

This script will raise an `AssertionError` and print the stack trace if the issue is present.