Here is the reproducer script:

```python
import sympy

def reproduce_issue():
    v1_5_1_result = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()
    v1_6_2_result = sympy.sympify('4*ceiling(x/4 - 3/4)', evaluate=False).simplify()

    if v1_5_1_result == '4*ceiling(x/4 - 3/4)' and v1_6_2_result != '4*ceiling(x/4) - 3':
        raise AssertionError("Inconsistent behavior for sympify/simplify with ceiling")

if __name__ == "__main__":
    try:
        reproduce_issue()
    except AssertionError as e:
        print_stacktrace(e)
        exit(1)
    else:
        exit(0)

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

```

This script will raise an AssertionError if the behavior of sympify/simplify with ceiling is not consistent between Sympy v1.5.1 and Sympy v1.6.2.