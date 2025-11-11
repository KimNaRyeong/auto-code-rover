import sympy as sp
from functools import wraps

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

def assert_raises(expected_exception, func, *args, **kwargs):
    try:
        func(*args, **kwargs)
        raise AssertionError("Expected an exception but got nothing")
    except expected_exception as e:
        return

try:
    f = (sp.sympify('x') - 2) / ((sp.sympify('x'))**2 + 1)
    degree(f, 'x')
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Expected SymPy to compute degrees of rational functions")

print("Reproducer finished. If you see this message, the issue is not present.")
