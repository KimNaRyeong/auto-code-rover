from sympy import *
import traceback
import sys

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

def bool_map(f1, f2):
    return (f1.lhs - f1.rhs).simplify(), {k: v for k, v in zip(f1.free_symbols, f2.free_symbols)}

A1, A2 = symbols('A1,A2')
f1 = Xor(A1, A2)
f2 = Not(Xor(A1, A2))

try:
    from sympy import *
    result1, _ = bool_map(f2, f1)
    result2, _ = bool_map(f1, f2)

    if result1 != '((A1 & ~A2) | (A2 & ~A1))' or result2 != '((A1 & A2) | (~A1 & ~A2))':
        raise AssertionError("Issue present")
except Exception as e:
    print_stacktrace(e)
    exit(1)

print("Issue fixed, reproducer script exiting with code 0")
exit(0)
