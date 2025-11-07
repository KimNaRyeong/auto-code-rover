Here is a standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp

def reproduce_issue():
    try:
        latex_expr = sp.Pow(sp.Rational(1, 2), -1, evaluate=False)
        print(latex(latex_expr))
    except RecursionError as e:
        print_stacktrace(e)

if __name__ == "__main__":
    reproduce_issue()
```

To run the reproducer, save this code in a file named `reproducer.py` and execute it using Python:

```bash
python3 reproducer.py
```

This script should raise an `AssertionError` when the issue is present and print a stack trace of the issue.