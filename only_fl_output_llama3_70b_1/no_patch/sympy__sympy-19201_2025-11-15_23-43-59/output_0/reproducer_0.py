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
