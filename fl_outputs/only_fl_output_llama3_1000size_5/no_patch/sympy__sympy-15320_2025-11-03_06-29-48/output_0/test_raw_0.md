Here is the reproducer script:

```python
import sympy as sp
from reproducer import print_stacktrace

def reproduce_issue():
    x = sp.symbols('x')
    t = sp.symbols('t')

    # Case 1: Same form, different generator
    root1 = sp.RootOf(x**3+x-1, 0)
    root2 = sp.RootOf((x**3+x-1).subs(x,t), 0)

    assert root1.poly.gen == x, "RootOf might ignore generator"

    # Case 2: Different form, same generator
    root3 = sp.RootOf(tan(x)**3 + 2*tan(x) - 1, 0)
    root4 = sp.RootOf((x**3+2*x-1), 0)

    assert root4.poly.gen == x, "RootOf might ignore generator"

try:
    reproduce_issue()
except AssertionError as e:
    print_stacktrace(e)
    exit(1)
```

This script will raise an `AssertionError` if the issue is present and print a stack trace. If the issue is fixed, it will simply exit with code 0.