Here is the `reproducer.py` file that reproduces the issue:
```python
import sympy as sp
from sympy import Mul, I

def main():
    x = sp.symbols('x')
    y = sp.symbols('y')

    # Reproduce the first bug
    try:
        result = (-2*x - 4*y - 8).extract_multiplicatively(-2)
        assert False, "Expected ValueError"
    except Exception as e:
        print_stacktrace(e)

    # Reproduce the second bug
    try:
        result = (2*x + 4*y + 8).extract_multiplicatively(-2)
        assert False, "Expected ValueError"
    except Exception as e:
        print_stacktrace(e)

if __name__ == '__main__':
    main()
```
This script defines a `main` function that attempts to reproduce the two bugs by calling `extract_multiplicatively` with `-2` as the argument. If an exception is raised, it prints the stack trace using the `print_stacktrace` function.

To run this script, save it in a file named `reproducer.py` and execute it with Python 3: `python3 reproducer.py`. This should print the stack trace of the bugs to the console.