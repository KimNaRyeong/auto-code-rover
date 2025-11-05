Here is the reproducer script:

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

def reproduce_issue():
    try:
        x, y = sympy.symbols('x, y')
        for i in [0.0215, 0.0216, 0.0217]:
            result = sympy.linsolve([sympy.Eq(y, x), sympy.Eq(y, i * x)], (x, y))
            if len(result) > 1:
                raise AssertionError("linsolve failed to return the expected result")
    except Exception as e:
        print_stacktrace(e)
        exit(1)

if __name__ == '__main__':
    reproduce_issue()
```

This script will run the `linsolve` function with different values of `i` and check if it returns more than one element. If so, it will raise an AssertionError and print the stack trace.