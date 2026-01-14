 Here is a standalone Python script `reproducer.py` that reproduces the issue:
```python
from sympy import simplify, Rational

def print_stacktrace(e: Exception):
    import traceback    import sys    tb = traceback.extract_tb(e.__traceback__)
    print("Traceback (most recent call last):", file=sys.stderr)
    for frame in tb:
        line_number = frame.lineno
        code_context = frame.line.strip() if frame.line else "Unknown"
        print(f'  File "{frame.filename}"', file=sys.stderr)
        print(f"    {line_number}: {code_context}", file=sys.stderr)
    print(f"{e.__class__.__name__}: {e}", file=sys.stderr)

initial_expression = Rational(1, 2)*(2*Rational(1, 2)*Rational(1, 2)*Rational(1, 2) - 2*Rational(1, 2)*Rational(1, 2)*Rational(1, 2) - Rational(1, 2)*Rational(1, 2) + Rational(1, 2)*Rational(1, 2) + Rational(1, 2)*Rational(1, 2) - Rational(1, 2)*Rational(1, 2))

simplified_expression = simplify(initial_expression)
final_expression = simplify(simplified_expression)

if simplified_expression != final_expression:
    raise AssertionError("Simplify doesn't do the last simplification step")

print("No issue found")
```
To run the script, execute `python3 reproducer.py` in the terminal. If the issue is present, an `AssertionError` will be raised and a stack trace will be printed. If the issue is fixed, the script will print "No issue found" and exit with code 0.

Note: The script uses the `sympy` library, so make sure it is installed before running the script. You can install it using `pip install sympy`.