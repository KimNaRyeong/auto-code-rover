```python
def print_stacktrace(e: Exception):
    import traceback
    import sys
    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

def test_sympy_integer_floor_division():
    import sympy
    s0 = sympy.Symbol('s0')
    try:
        result = sympy.Integer(1024)//s0
        # The following assertion checks if the issue exists.
        # If the code above succeeds without throwing an exception,
        # then it means the issue doesn't exist and we shouldn't hit this assertion.
        assert False, "Expected a TypeError"
    except TypeError as e:
        print_stacktrace(e)

if __name__ == '__main__':
    test_sympy_integer_floor_division()
```

- The function `test_sympy_integer_floor_division` replicates the issue of attempting floor division using a `sympy.Integer` and a symbolic expression. 
- In a scenario where the underlying sympy behavior is unchanged and still raises a `TypeError`, the script prints a detailed stack trace. 
- The assertion is there to fail explicitly if for some reason the operation succeeds without an error, signaling that the reported issue has been resolved (or perhaps not correctly replicated).
- When executed, this script should exit with code 0 if the reported issue is present. However, if by any means the issue was already solved in the library being used (i.e., the problematic operation does not raise an error), the script will raise an `AssertionError`.