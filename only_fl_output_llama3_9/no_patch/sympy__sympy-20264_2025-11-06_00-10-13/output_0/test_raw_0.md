Here is the reproducer script:

```python
import sympy as sp
from sympy import Rational, Pow

def reproduce_issue():
    try:
        latex_expr = Pow(Rational(1, 2), -1, evaluate=False)
        print(latex_expr)
    except RecursionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

You can run this script using `python3 reproducer.py`. If the issue is present, it will raise a `RecursionError` and print the stack trace.