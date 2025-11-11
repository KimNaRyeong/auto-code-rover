Here is the standalone Python file `reproducer.py` that reproduces the issue:

```python
import sympy as sp
from reproducer import print_stacktrace

def main():
    b = 1 - sp.sqrt(2)
    a = sp.to_number_field(b)
    if not (a.minpoly.as_poly().as_coeff_Mul()[0].as_expr() == _x**2 + 2*_x - 1):
        raise AssertionError("Issue present")
    print_stacktrace(Exception())

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        print("Issue fixed")
        exit(0)
```

This script creates the algebraic number `b` and then calls `to_number_field` to create an `AlgebraicNumber` generating the extension field. It checks if the minimal polynomial of this generated number is correct, and if not, raises an `AssertionError`. The `print_stacktrace` function is used to print the stack trace of the issue.

To run the script, save it in a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`.