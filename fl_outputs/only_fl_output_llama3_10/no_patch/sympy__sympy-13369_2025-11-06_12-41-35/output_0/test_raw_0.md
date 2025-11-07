Here is the reproducer script:

```python
import sympy as sp
from sympy import Symbol, Matrix, eye
from functools import wraps

def assert_raises(expected_exception):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except expected_exception as e:
                print_stacktrace(e)
                raise AssertionError("Expected exception not raised")
            else:
                raise AssertionError("Expected exception not raised")
        return wrapper
    return decorator

@assert_raises(sp.matrices.common.MatrixError)
def reproduce_issue():
    x = Symbol('x')
    M = Matrix([[x, 0, 1], [x, 0, 2], [sp.exp(x), 1, 0]])
    try:
        M.eigenvals()
    except Exception as e:
        print_stacktrace(e)
        raise

if __name__ == "__main__":
    reproduce_issue()
```

This script will run the reproducer function and if it raises a `sympy.matrices.common.MatrixError`, it will print the stack trace and then raise an `AssertionError`.