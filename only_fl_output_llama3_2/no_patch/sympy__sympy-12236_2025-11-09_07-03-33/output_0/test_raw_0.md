Here is the reproducer script:

```python
import sympy
from sympy import symbols

def main():
    a = symbols('a', real=True)
    t = symbols('t', real=True, negative=False)
    bug = a * (-t + (-t + 1) * (2 * t - 1)) / (2 * t - 1)

    try:
        print(bug.subs(a, 1).apart(t))
        assert bug.apart(t) == bug.subs(a, 1).apart(t)
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)

if __name__ == "__main__":
    sympy.__version__ = '1.0'
    main()
```

This script will raise an `AssertionError` if the result of `bug.apart(t)` is not equal to the result of `(bug.subs(a, 1)).apart(t)`, and print a stack trace with line numbers.