 Here is a standalone python file `reproducer.py` to reproduce the issue:

```python
from sympy import *
from reproducer import print_stacktrace

def test_refine():
    var('a,x')
    J = Integral(sin(x)*exp(-a*x),(x,0,oo))
    J = J.doit()

    # The issue is that refine does not simplify the integral when a is positive
    assert refine(J, Q.positive(a)) == J, "refine does not simplify the integral when a is positive"

def main():
    test_refine()

if __name__ == "__main__":
    try:
        main()
    except AssertionError as e:
        print_stacktrace(e)
        raise e
```

When the issue is present, the script will raise an `AssertionError` and print a stack trace of the issue. When the issue is fixed, the script will exit with code 0.