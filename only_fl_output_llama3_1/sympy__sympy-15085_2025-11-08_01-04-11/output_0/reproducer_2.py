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

try:
    from sympy import Symbol, Matrix
    x = Symbol("x")
    expr = dot(x, Matrix([[2], [1], [0]]))
    f = sympy.lambdify(x, expr)
    X = numpy.zeros((17, 3))
    val = f(X)
except Exception as e:
    print_stacktrace(e)
    raise AssertionError("Issue present")
else:
    print("Issue fixed")
    exit(0)

class dot(sympy.Function):
    pass
