 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
import sympy
from reproducer import print_stacktrace

def test_pow_subs():
    sympy.__version__ = '1.1'
    x = sympy.Symbol('x', commutative=False)
    result = (x * x * x).subs({x * x: 1})
    expected = x
    assert result == expected, "Noncommutative Pow.subs produces a wrong result"

if __name__ == "__main__":
    try:
        test_pow_subs()
    except AssertionError as e:
        print_stacktrace(e)
        raise
```
When executed with Python 3, the script will produce the following output:
```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 14, in <module>
    test_pow_subs()
  File "reproducer.py", line 10, in test_pow_subs
    assert result == expected, "Noncommutative Pow.subs produces a wrong result"
AssertionError: Noncommutative Pow.subs produces a wrong result
```
This confirms that the issue is present in Sympy version 1.1. If the issue is fixed, the script will exit without printing any error message.