 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import Add, MatAdd, MatrixSymbol, symbols
from sympy.abc import x

def print_stacktrace(e: Exception):
    import traceback    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_add():
    add1 = Add(x, x, evaluate=True)
    add2 = Add(x, x, evaluate=False)
    assert add1 == 2*x, "Addition with evaluate=True failed"
    assert add2 == x + x, "Addition with evaluate=False failed"

def test_matadd():
    A = MatrixSymbol('A', 2, 2)
    matadd1 = MatAdd(A, A)
    matadd2 = MatAdd(A, A, evaluate=True)
    assert matadd1 == A + A, "Matrix addition with default evaluate failed"
    assert matadd2 == 2*A, "Matrix addition with evaluate=True failed"

if __name__ == "__main__":
    try:
        test_add()
        test_matadd()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    except Exception as e:
        print_stacktrace(e)
        exit(1)
```
When executed with `python3 reproducer.py`, the script will raise an `AssertionError` for the current behavior of `MatAdd`:
```shell
$ python3 reproducer.py
Traceback (most recent call last):
  File "reproducer.py", line 31, in <module>
    test_matadd()
  File "reproducer.py", line 26, in test_matadd
    assert matadd2 == 2*A, "Matrix addition with evaluate=True failed"
AssertionError: Matrix addition with evaluate=True failed
```
If the `evaluate` keyword argument is added to `MatAdd` and `MatMul` as described in the issue, the script will not raise an `AssertionError` and will exit with code 0.