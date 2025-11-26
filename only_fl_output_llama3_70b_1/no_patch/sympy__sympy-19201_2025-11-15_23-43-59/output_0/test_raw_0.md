Here is the `reproducer.py` file to reproduce the issue:
```
import sympy as sp
from sympy import MatrixSymbol, pprint

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

n = 5
A = MatrixSymbol('A', n, n)
B = MatrixSymbol('B', n, n)

expected_outputs = {
    'A[:, :]': 'A[:, :]',
    'A[:5, :5]': 'A[:5, :5]',
    'A[5:, 5:]': 'A[5:, 5:]',
    'A[::2, ::2]': 'A[::2, ::2]',
    'A[1:2, 1:2]': 'A[1:2, 1:2]',
    'A[:1, :1]': 'A[0, 0]',
    'A[:1:2, :1:2]': 'A[0, 0]',
}

for expr_str, expected_output in expected_outputs.items():
    expr = eval(expr_str)
    try:
        output = str(expr)
        assert output == expected_output, f"Expected {expected_output} but got {output}"
    except AssertionError as e:
        print_stacktrace(e)
        raise SystemExit(1)

try:
    composite_expr = (A + B)[:2, :2]
    output = str(composite_expr)
    assert output.startswith('(') and output.endswith(')'), "Expected brackets around the composite expression"
except AssertionError as e:
    print_stacktrace(e)
    raise SystemExit(1)

print("All tests passed!")
```
This script defines a set of expected outputs for various slice expressions involving `MatrixSymbol` objects. It then evaluates each expression, converts it to a string using the `str()` function, and asserts that the output matches the expected output. If any assertion fails, it prints a stack trace of the error using the provided `print_stacktrace()` function and exits with code 1.

Additionally, the script tests that brackets are properly printed around composite expressions involving matrix slices. If this test fails, it also prints a stack trace and exits with code 1.

If all tests pass, the script prints "All tests passed!" and exits with code 0.